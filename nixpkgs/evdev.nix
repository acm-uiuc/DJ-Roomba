with import <nixpkgs> {};


python3Packages.buildPythonPackage rec {
    version = "0.4.7";
    name = "evdev-${version}";
    
    src = pkgs.fetchurl {
        url = "https://pypi.python.org/packages/source/e/evdev/${name}.tar.gz";
        sha256 = "339c5bfadfa92dc50786ac6bdfacdb8061ad01bdea482be6e281f5cbac63e8d7";
    };

    buildInputs = with self; [ pkgs.linuxHeaders ];
    patchPhase = "sed -e 's#/usr/include/linux/input.h#${pkgs.linuxHeaders}/include/linux/input.h#' -i setup.py";
    doCheck = false;
    meta = with stdenv.lib; {
    description = "Provides bindings to the generic input event interface in Linux";
    homepage = http://pythonhosted.org/evdev;
    license = licenses.bsd3;
    maintainers = [ maintainers.goibhniu ];
    platforms = stdenv.lib.platforms.linux;
};}
