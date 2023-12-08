from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("port", 8080, "port to run Python server on")


def port():
  return FLAGS.port
