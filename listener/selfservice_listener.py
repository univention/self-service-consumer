import os

from univention.listener.handler import ListenerModuleHandler

cache_dir = "/var/cache/listener"


class SelfserviceListener(ListenerModuleHandler):
    """
    Listener module that creates a file on a folder if the newly created user
    has the class `univentionPasswordSelfServiceEmail`.
    """

    def initialize(self):
        self.logger.info("[ initialize ] SelfserviceListener")

    def create(self, dn, new):
        self.logger.info("[ create ] dn: %r", dn)
        key, uid = dn.split(",")[0].split("=")
        assert key == "uid"
        filename = os.path.join(cache_dir, uid.replace("/", "") + ".send")
        self.logger.debug(
            "Trigger selfservice invitation for %r" % (dn),
        )
        try:
            os.mknod(filename)
        except OSError as exc:
            if hasattr(exc, "errno") and exc.errno == 17:
                pass
            else:
                raise

    class Configuration(ListenerModuleHandler.Configuration):
        name = "selfservice-listener"
        description = "Self Service user invite listener"
        ldap_filter = "(objectClass=univentionPasswordSelfService)"
