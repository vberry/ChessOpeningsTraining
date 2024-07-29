import pkg_resources, os, time

for package in pkg_resources.working_set:
    infos = "%s:     %s" % (package, time.ctime(os.path.getctime(package.location)))
    #if infos.contains('28'):
    if '2024' in infos:
            print(infos)
    #print(infos)


