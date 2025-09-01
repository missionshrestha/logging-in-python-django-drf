import logging
import module_a
import module_b

# Configure root logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)-20s | %(levelname)-8s | %(message)s"
)

module_a.run_a()
module_b.run_b()
