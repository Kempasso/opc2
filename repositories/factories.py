from repositories import Fabric
from tables import Device, Code, Signal, SignalsLog

device_fabric = Fabric(table=Device, ignore_fields=["codes"])
devices_fabric = Fabric(table=Device, ignore_fields=["codes"], many=True)

signal_fabric = Fabric(table=Signal, ignore_fields=["code"],
                       child_fabrics={"device_id": device_fabric})
signal_fabric = Fabric(table=Signal, ignore_fields=["code"],
                       child_fabrics={"device_id": device_fabric}, many=True)
# signal_log_fabric = Fabric(table=SignalsLog, ignore_fields=["device"])
# signals_log_fabric = Fabric(table=SignalsLog, ignore_fields=["device"], many=True)
signal_log_fabric = Fabric(
    table=SignalsLog,
    ignore_fields=["signal"],
    child_fabrics={"signal_id": signal_fabric},
)

code_fabric = Fabric(table=Code,
                     ignore_fields=["device", "signal"],
                     child_fabrics={"device_id": device_fabric,
                                    "signal_id": signal_fabric})
codes_fabric = Fabric(table=Code,
                      ignore_fields=["device", "signal"],
                      child_fabrics={"device_id": device_fabric,
                                     "signal_id": signal_fabric},
                      many=True)
