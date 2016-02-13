from zipfile import ZipFile

from jawa.cf import ClassFile


def class_name_to_filesystem_name(class_name):
    return class_name.replace('.', '/') + '.class'


def filesystem_name_to_class_name(filesystem_name):
    if not filesystem_name.endswith('.class'):
        raise ValueError("{} doesn't end in .class".format(filesystem_name))

    return filesystem_name[:-len('.class')].replace('/', '.')


class SpongePoweredPlugin(object):

    def __init__(self, classname, kvps):
        self.classname = classname
        self.data = {
            'id': None,
            'name': None,
            'version': None
        }
        self.data.update(kvps)

    def validate(self):
        errors = []

        if not self.data['id']:
            errors.append('No "id" attribute set')

        if not self.data['name']:
            errors.append('No "name" attribute set')

        if not self.data['version']:
            errors.append('No "version" attribute set')

        return errors

    def __repr__(self):
        return "SpongePoweredPlugin(classname={0!r}, data={1!r})".format(self.classname, self.data)


class Plugalyzer(object):

    def __init__(self, zf):
        self.zipfile = zf
        self._cache = {}

    def run(self):
        return list(self.find_plugin_classes())


    def find_plugin_classes(self):
        for filename in filter(lambda fn: fn.endswith('.class'), self.zipfile.namelist()):
            spp = self.is_spongepowered_plugin(filename)
            if spp:
                yield SpongePoweredPlugin(filesystem_name_to_class_name(filename), spp)

    def is_spongepowered_plugin(self, filename):
        cf = self.analyze_class_file(filename)
        rva = cf.attributes.find_one('RuntimeVisibleAnnotations')
        if not rva:
            return False

        plugin_annotations = [(a.type, a.key_value_pairs) for a in rva.annotations if a.type == 'Lorg/spongepowered/api/plugin/Plugin;']
        if not plugin_annotations:
            return False

        return plugin_annotations[0][1]

    def analyze_class_file(self, filename):
        if filename in self._cache:
            return self._cache[filename]

        with self.zipfile.open(filename, 'r') as cf_fp:
            cf = ClassFile(cf_fp)
            self._cache[filename] = cf
            return cf

    @classmethod
    def analyze(self, fp_or_filename):
        with ZipFile(fp_or_filename, 'r') as jf:
            return Plugalyzer(jf).run()


if __name__ == '__main__':
    import sys

    def usage():
        print("{} [JAR file path]".format(sys.argv[0]))
        sys.exit(1)

    if len(sys.argv) != 2:
        usage()

    plugalyzer = Plugalyzer.analyze(sys.argv[1])
    print(sys.argv[1], plugalyzer)
