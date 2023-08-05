from collections import OrderedDict
import logging
from neo4j.v1 import GraphDatabase
import neobolt.exceptions
import time

import cartography.intel.analysis
import cartography.intel.aws
import cartography.intel.create_indexes


logger = logging.getLogger(__name__)


class Sync(object):
    """
    A cartography sync task.

    The role of the sync task is to ensure the data in the graph database represents reality. It does this by executing
    a sequence of sync "stages" which are responsible for retrieving data from various sources (APIs, files, etc.),
    pushing that data to Neo4j, and removing now-invalid nodes and relationships from the graph. An instance of this
    class can be configured to run any number of stages in a specific order.
    """
    def __init__(self):
        # NOTE we may need meta-stages at some point to allow hooking into pre-sync, sync, and post-sync
        self._stages = OrderedDict()

    def add_stage(self, name, func):
        """
        Add one stage to the sync task.

        :type name: string
        :param name: The name of the stage.
        :type func: Callable
        :param func: The object to call when the stage is executed.
        """
        self._stages[name] = func

    def add_stages(self, stages):
        """
        Add multiple stages to the sync task.

        :type stages: List[Tuple[string, Callable]]
        :param stages: A list of stage names and stage callable pairs.
        """
        for name, func in stages:
            self.add_stage(name, func)

    def run(self, neo4j_driver, config):
        """
        Execute all stages in the sync task in sequence.

        :type neo4j_driver: neo4j.Driver
        :param neo4j_driver: Neo4j driver object.
        :type config: cartography.config.Config
        :param config: Configuration for the sync run.
        """
        logger.info("Starting sync with update tag '%d'", config.update_tag)
        with neo4j_driver.session() as neo4j_session:
            for stage_name, stage_func in self._stages.items():
                logger.info("Starting sync stage '%s'", stage_name)
                try:
                    stage_func(neo4j_session, config)
                except (KeyboardInterrupt, SystemExit):
                    logger.warning("Sync interrupted during stage '%s'.", stage_name)
                    raise
                except Exception:
                    logger.exception("Unhandled exception during sync stage '%s'", stage_name)
                    raise  # TODO this should be configurable
                logger.info("Finishing sync stage '%s'", stage_name)
        logger.info("Finishing sync with update tag '%d'", config.update_tag)


def run_with_config(sync, config):
    """
    Execute the cartography.sync.Sync.run method with parameters built from the given configuration object.

    This function will create a Neo4j driver object from the given Neo4j configuration options (URI, auth, etc.) and
    will choose a sensible update tag if one is not specified in the given configuration.

    :type sync: cartography.sync.Sync
    :param sync: A sync task to run.
    :type config: cartography.config.Config
    :param config: The configuration to use to run the sync task.
    """
    neo4j_auth = None
    if config.neo4j_user or config.neo4j_password:
        neo4j_auth = (config.neo4j_user, config.neo4j_password)
    try:
        neo4j_driver = GraphDatabase.driver(
            config.neo4j_uri,
            auth=neo4j_auth,
        )
    except neobolt.exceptions.ServiceUnavailable as e:
        logger.debug("Error occurred during Neo4j connect.", exc_info=True)
        logger.error(
            (
                "Unable to connect to Neo4j using the provided URI '%s', an error occurred: '%s'. Make sure the Neo4j "
                "server is running and accessible from your network."
            ),
            config.neo4j_uri,
            e
        )
        return
    except neobolt.exceptions.AuthError as e:
        logger.debug("Error occurred during Neo4j auth.", exc_info=True)
        if not neo4j_auth:
            logger.error(
                (
                    "Unable to auth to Neo4j, an error occurred: '%s'. cartography attempted to connect to Neo4j "
                    "without any auth. Check your Neo4j server settings to see if auth is required and, if it is, "
                    "provide cartography with a valid username and password."
                ),
                e
            )
        else:
            logger.error(
                (
                    "Unable to auth to Neo4j, an error occurred: '%s'. cartography attempted to connect to Neo4j with "
                    "a username and password. Check your Neo4j server settings to see if the username and password "
                    "provided to cartography are valid credentials."
                ),
                e
            )
        return
    default_update_tag = int(time.time())
    if not config.update_tag:
        config.update_tag = default_update_tag
    return sync.run(neo4j_driver, config)


def build_default_sync():
    """
    Build the default cartography sync, which runs all intelligence modules shipped with the cartography package.

    :rtype: cartography.sync.Sync
    :return: The default cartography sync object.
    """
    sync = Sync()
    sync.add_stages([
        ('create-indexes', cartography.intel.create_indexes.run),
        ('aws', cartography.intel.aws.start_aws_ingestion),
        ('analysis', cartography.intel.analysis.run),
    ])
    return sync
