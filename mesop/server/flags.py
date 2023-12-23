from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("port", 32123, "port to run Python server on")


def port():
  return FLAGS.port
