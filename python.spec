%global tapsetdir      /usr/share/systemtap/tapset
%global PyIncludeDirs python%{pybasever}
%global unicode ucs4
%global _default_patch_fuzz 2
%global python python
%global tkinter tkinter
%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global tools_dir %{pylibdir}/Tools
%global demo_dir %{pylibdir}/Demo
%global doc_tools_dir %{pylibdir}/Doc/tools
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{pybasever}.so.%{py_SOVERSION}
%global __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
    /usr/lib/rpm/redhat/brp-java-repack-jars \
    %{nil}
%global run_selftest_suite 0
%global _python_bytecompile_errors_terminate_build 0
%global regenerate_autotooling_patch 0

Summary: An interpreted, interactive, object-oriented programming language
Name: %{python}
Version: 2.7.11
Release: 1.%{dist}
License: Python
Vendor: %{vendor}
Packager: %{packager}
Group: Development/Languages
Requires: %{python}-libs%{?_isa} = %{version}-%{release}
Requires: expat
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
Provides: %{name} = %{version}
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: redhat-rpm-config expat-devel
BuildRequires: expat-devel
BuildRequires: findutils
BuildRequires: clang 
BuildRequires: gdbm-devel
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: systemtap-sdt-devel
BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel
BuildRequires: valgrind-devel
BuildRequires: zlib-devel

Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source2: pythondeps.sh
%global __python_requires %{SOURCE2}
Source3: libpython.stp
Source4: systemtap-example.stp
Source5: pyfuntop.stp
Source6: macros.python27
Source7: macros.python27_build
Patch1: Python-2.2.1-pydocnogui.patch
Patch4: python-2.5-cflags.patch
Patch10: python-2.7rc1-binutils-no-dep.patch
Patch13: python-2.7rc1-socketmodule-constants.patch
#Patch54: python-2.6.4-setup-db48.patch
Patch102: python-2.7.3-lib64.patch
Patch103: python-2.7-lib64-sysconfig.patch
Patch104: 00104-lib64-fix-for-test_install.patch
Patch111: 00111-no-static-lib.patch


Patch113: 00113-more-configuration-flags.patch
Patch114: 00114-statvfs-f_flag-constants.patch
Patch125: 00125-less-verbose-COUNT_ALLOCS.patch
Patch128: python-2.7.1-fix_test_abc_with_COUNT_ALLOCS.patch
Patch130: python-2.7.2-add-extension-suffix-to-python-config.patch
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch
Patch133: 00133-skip-test_dl.patch
Patch134: 00134-fix-COUNT_ALLOCS-failure-in-test_sys.patch
Patch135: 00135-skip-test-within-test_weakref-in-debug-build.patch
Patch137: 00137-skip-distutils-tests-that-fail-in-rpmbuild.patch
Patch138: 00138-fix-distutils-tests-in-debug-build.patch
Patch139: 00139-skip-test_float-known-failure-on-arm.patch
Patch140: 00140-skip-test_ctypes-known-failure-on-sparc.patch
Patch141: 00141-fix-test_gc_with_COUNT_ALLOCS.patch
Patch142: 00142-skip-failing-pty-tests-in-rpmbuild.patch
Patch143: 00143-tsc-on-ppc.patch
Patch155: 00155-avoid-ctypes-thunks.patch
Provides: Distutils
Provides: python2 = %{version}
Provides: python-sqlite = 2.3.2
Provides: python-ctypes = 1.0.1
Provides: python-hashlib = 20081120
Provides: python-uuid = 1.31
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://www.python.org/

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface.

Note that documentation for Python is provided in the python-docs
package.

This package provides the "python" executable; most of the actual
implementation is within the "python-libs" package.

%package libs
Summary: Runtime libraries for Python
Group: Applications/System
Requires: expat

%description libs
This package contains runtime libraries for use by Python:
- the libpython dynamic library, for use by applications that embed Python as
a scripting language, and by the main "python" executable
- the Python standard library

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{python}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{tkinter} = %{version}-%{release}

%description tools
This package includes several tools to help with the development of Python   
programs, including IDLE (an IDE with editing and debugging facilities), a 
color editor (pynche), and a python gettext program (pygettext.py).  

%package -n %{tkinter}
Summary: A graphical user interface for the Python scripting language
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description -n %{tkinter}

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.

%package pip
Summary: A package management system used to install and manage software packages written in Python
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description pip
pip is a package management system used to install and manage software packages written in Python. Many packages can be found in the Python Package Index (PyPI). Python 2.7.9 and later (on the python2 series), and Python 3.4 and later include pip (pip3 for Python 3) by default.

%prep
%setup -q -n Python-%{version}
cp -a %{SOURCE4} .
cp -a %{SOURCE5} .
rm -r Modules/expat || exit 1
rm -r Modules/zlib || exit 1
for f in md5module.c md5.c shamodule.c sha256module.c sha512module.c; do
    rm Modules/$f
done
%patch1 -p1 -b .no_gui
%patch4 -p1 -b .cflags
# patch101: upstream as of Python 2.7.4
%patch102 -p1 -b .lib64
%patch103 -p1 -b .lib64-sysconfig
%patch104 -p1
%patch10 -p1 -b .binutils-no-dep
%patch13 -p1 -b .socketmodule
#%patch54 -p1 -b .setup-db48
%patch111 -p1 -b .no-static-lib
%patch113 -p1 -b .more-configuration-flags
%patch114 -p1 -b .statvfs-f-flag-constants
%patch125 -p1 -b .less-verbose-COUNT_ALLOCS
%patch128 -p1
%patch130 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch137 -p1
%patch138 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1 -b .tsc-on-ppc
%patch155 -p1
find -name "*~" |xargs rm -f

%build
topdir=$(pwd)
export CXX="/usr/bin/g++"
export CC="/usr/bin/gcc"
export LINKCC="/usr/bin/gcc"
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LDFLAGS="$RPM_LD_FLAGS"
if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
  export LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi

%if 0%{regenerate_autotooling_patch}
for f in pyconfig.h.in configure ; do
    cp $f $f.autotool-intermediates ;
done
PATH=~/autoconf-2.65/bin:$PATH autoconf
autoheader
gendiff . .autotool-intermediates > %{PATCH5000}
exit 1
%endif

BuildPython() {
  ConfName=$1	      
  BinaryName=$2
  SymlinkName=$3
  ExtraConfigArgs=$4
  PathFixWithThisBinary=$5
  ConfDir=build/$ConfName
  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir
  pushd $ConfDir
  %global configure $topdir/configure

%configure \
  --prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --sysconfdir=/etc \
  --enable-ipv6 \
  --enable-shared \
  --enable-unicode=%{unicode} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --with-dtrace \
  --with-tapset-install-dir=%{tapsetdir} \
  --with-valgrind \
  --includedir=%{_includedir} \
  --enable-profiling \
  --with-threads \
  --with-pth \
  --with-ensurepip="upgrade" 
  $ExtraConfigArgs \
  %{nil}

  make EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}
  if $PathFixWithThisBinary
  then
    LD_LIBRARY_PATH="$topdir/$ConfDir" ./$BinaryName $topdir/Tools/scripts/pathfix.py -i "%{_bindir}/env $BinaryName" $topdir
  fi
  #ln -s $BinaryName $SymlinkName
  LD_LIBRARY_PATH="$topdir/$ConfDir" PATH=$PATH:$topdir/$ConfDir make -s EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}
  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfDir
}

BuildPython optimized python python "" true

%install
topdir=$(pwd)
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}
for f in distutils/command/install distutils/sysconfig; do
    rm -f Lib/$f.py.lib64
done
InstallPython() {
  ConfName=$1	      
  BinaryName=$2
  PyInstSoName=$3
  ConfDir=build/$ConfName
  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir
  pushd $ConfDir
  make install DESTDIR=%{buildroot}
  DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
  PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName.debug-gdb.py
  mkdir -p %{buildroot}$DirHoldingGdbPy
  cp $topdir/Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
  LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"
  LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName -O -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"
  popd
  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

InstallPython optimized python %{py_INSTSONAME_optimized}

for fixed in %{buildroot}%{_bindir}/pydoc; do
    sed 's,#!.*/python$,#!%{_bindir}/env python,' $fixed > $fixed- && cat $fixed- > $fixed && rm -f $fixed-
done

rm -f %{buildroot}/%{pylibdir}/idlelib/testcode.py*
if /bin/false; then
mkdir save_bits_of_test
for i in test_support.py __init__.py; do
  cp -a %{buildroot}/%{pylibdir}/test/$i save_bits_of_test
done
rm -rf %{buildroot}/%{pylibdir}/test
mkdir %{buildroot}/%{pylibdir}/test
cp -a save_bits_of_test/* %{buildroot}/%{pylibdir}/test
fi

mkdir -p ${RPM_BUILD_ROOT}%{site_packages}
cat > ${RPM_BUILD_ROOT}%{_bindir}/pynche << EOF
#!/bin/bash
exec %{site_packages}/pynche/pynche
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/pynche
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche ${RPM_BUILD_ROOT}%{site_packages}/
mv Tools/pynche/README Tools/pynche/README.pynche
install -m755  Tools/i18n/pygettext.py %{buildroot}%{_bindir}/
install -m755  Tools/i18n/msgfmt.py %{buildroot}%{_bindir}/
install -m755 -d %{buildroot}%{tools_dir}/scripts
install Tools/README %{buildroot}%{tools_dir}/
install Tools/scripts/*py %{buildroot}%{tools_dir}/scripts/
install -m755 -d %{buildroot}%{doc_tools_dir}
install -m755 -d %{buildroot}%{demo_dir}
cp -ar Demo/* %{buildroot}%{demo_dir}
find %{buildroot}/ -name "*~"|xargs rm -f
find %{buildroot}/ -name ".cvsignore"|xargs rm -f
find %{buildroot}/ -name "*.bat"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
rm -rf %{buildroot}%{_mandir}/man1/python.1
rm -f %{buildroot}%{pylibdir}/LICENSE.txt
pushd %{buildroot}%{_bindir}
popd
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au
install -d %{buildroot}%{pylibdir}/site-packages
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h
%global _pyconfig_h %{_pyconfig64_h}

for PyIncludeDir in %{PyIncludeDirs} ; do
  mv %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h \
     %{buildroot}%{_includedir}/$PyIncludeDir/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
done
ln -s ../../libpython.so %{buildroot}%{pylibdir}/config/libpython.so

sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/rpm/macros.python
install -m 644 %{SOURCE7} %{buildroot}%{_rpmconfigdir}/macros.d/macros.python

ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)

for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *_d.so)
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)
            
        ;;
    *)
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_optimized} ; exit 1)
        ;;
    esac
done
mkdir -p %{buildroot}%{tapsetdir}
%global libpython_stp_optimized libpython-64.stp
%global libpython_stp_debug     libpython-debug-64.stp
sed -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_optimized}|" %{SOURCE3} > %{buildroot}%{tapsetdir}/%{libpython_stp_optimized}

if [ -d "%{buildroot}/usr/lib/debug" ]
then
  %__rm -rf %{buildroot}/usr/lib/debug
fi

for i in `find %{buildroot} -name 'RECORD'`
do
  sed -i -e "s|%{buildroot}||g" $i
done
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_mandir}/*/*

%files pip
%{_bindir}/easy_install
%{_bindir}/easy_install-%{pybasever}
%{_bindir}/pip
%{_bindir}/pip2
%{_bindir}/pip%{pybasever}
%{_usr}/lib/python%{pybasever}/site-packages/_markerlib/__init__.py
%{_usr}/lib/python%{pybasever}/site-packages/_markerlib/__init__.pyc
%{_usr}/lib/python%{pybasever}/site-packages/_markerlib/markers.py
%{_usr}/lib/python%{pybasever}/site-packages/_markerlib/markers.pyc
%{_usr}/lib/python%{pybasever}/site-packages/easy_install.py
%{_usr}/lib/python%{pybasever}/site-packages/easy_install.pyc
%{_usr}/lib/python%{pybasever}/site-packages/pip*
%{_usr}/lib/python%{pybasever}/site-packages/pkg_resources
%{_usr}/lib/python%{pybasever}/site-packages/setuptools*
%{pylibdir}/ensurepip*


%files libs
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/Python-%{version}-py%{pybasever}.egg-info
%{dynload_dir}/_bisect.so
%{dynload_dir}/_bsddb.so
%{dynload_dir}/_codecs_cn.so
%{dynload_dir}/_codecs_hk.so
%{dynload_dir}/_codecs_iso2022.so
%{dynload_dir}/_codecs_jp.so
%{dynload_dir}/_codecs_kr.so
%{dynload_dir}/_codecs_tw.so
%{dynload_dir}/_collections.so
%{dynload_dir}/_csv.so
%{dynload_dir}/_ctypes.so
%{dynload_dir}/_curses.so
%{dynload_dir}/_curses_panel.so
%{dynload_dir}/_elementtree.so
%{dynload_dir}/_functools.so
%{dynload_dir}/_hashlib.so
%{dynload_dir}/_heapq.so
%{dynload_dir}/_hotshot.so
%{dynload_dir}/_io.so
%{dynload_dir}/_json.so
%{dynload_dir}/_locale.so
%{dynload_dir}/_lsprof.so
%{dynload_dir}/_multibytecodec.so
%{dynload_dir}/_multiprocessing.so
%{dynload_dir}/_random.so
%{dynload_dir}/_socket.so
%{dynload_dir}/_sqlite3.so
%{dynload_dir}/_ssl.so
%{dynload_dir}/_struct.so
%{dynload_dir}/array.so
%{dynload_dir}/audioop.so
%{dynload_dir}/binascii.so
%{dynload_dir}/bz2.so
%{dynload_dir}/cPickle.so
%{dynload_dir}/cStringIO.so
%{dynload_dir}/cmath.so
%{dynload_dir}/crypt.so
%{dynload_dir}/datetime.so
%{dynload_dir}/dbm.so
%{dynload_dir}/fcntl.so
%{dynload_dir}/future_builtins.so
%{dynload_dir}/gdbm.so
%{dynload_dir}/grp.so
%{dynload_dir}/itertools.so
%{dynload_dir}/linuxaudiodev.so
%{dynload_dir}/math.so
%{dynload_dir}/mmap.so
%{dynload_dir}/nis.so
%{dynload_dir}/operator.so
%{dynload_dir}/ossaudiodev.so
%{dynload_dir}/parser.so
%{dynload_dir}/pyexpat.so
%{dynload_dir}/readline.so
%{dynload_dir}/resource.so
%{dynload_dir}/select.so
%{dynload_dir}/spwd.so
%{dynload_dir}/strop.so
%{dynload_dir}/syslog.so
%{dynload_dir}/termios.so
%{dynload_dir}/time.so
%{dynload_dir}/unicodedata.so
%{dynload_dir}/zlib.so

%dir %{site_packages}
%{site_packages}/README
%{pylibdir}/*.py*
%{pylibdir}/*.doc
%{pylibdir}/wsgiref.egg-info
%dir %{pylibdir}/bsddb
%{pylibdir}/bsddb/*.py*
%{pylibdir}/compiler
%dir %{pylibdir}/ctypes
%{pylibdir}/ctypes/*.py*
%{pylibdir}/ctypes/macholib
%{pylibdir}/curses
%dir %{pylibdir}/distutils
%{pylibdir}/distutils/*.py*
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%exclude %{pylibdir}/distutils/command/wininst-*.exe
%dir %{pylibdir}/email
%{pylibdir}/email/*.py*
%{pylibdir}/email/mime
%{pylibdir}/encodings
%{pylibdir}/hotshot
%{pylibdir}/idlelib
%{pylibdir}/importlib
%dir %{pylibdir}/json
%{pylibdir}/json/*.py*
%{pylibdir}/lib2to3
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%{pylibdir}/plat-linux2
%{pylibdir}/pydoc_data
%dir %{pylibdir}/sqlite3
%{pylibdir}/sqlite3/*.py*
%dir %{pylibdir}/test
%{pylibdir}/test/test_support.py*
%{pylibdir}/test/__init__.py*
%{pylibdir}/unittest
%{pylibdir}/wsgiref
%{pylibdir}/xml
%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif

%dir %{pylibdir}/config
%{pylibdir}/config/Makefile
%dir %{_includedir}/python%{pybasever}
%{_includedir}/python%{pybasever}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}
%{tapsetdir}/%{libpython_stp_optimized}
%doc systemtap-example.stp pyfuntop.stp

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python2.pc
%{pylibdir}/config/*
%exclude %{pylibdir}/config/Makefile
%{pylibdir}/distutils/command/wininst-*.exe
%{_includedir}/python%{pybasever}/*.h
%exclude %{_includedir}/python%{pybasever}/%{_pyconfig_h}
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_bindir}/python%{pybasever}-config
%{_libdir}/libpython%{pybasever}.so
%config(noreplace) %{_rpmconfigdir}/macros.d/macros.python
%config(noreplace) %{_sysconfdir}/rpm/macros.python

%files tools
%defattr(-,root,root,755)
%doc Tools/pynche/README.pynche
%{site_packages}/pynche
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*
%{_bindir}/pynche*
%{_bindir}/pygettext*.py*
%{_bindir}/msgfmt*.py*
%{tools_dir}
%{demo_dir}
%{pylibdir}/Doc

%files -n %{tkinter}
%defattr(-,root,root,755)
%{pylibdir}/lib-tk
%{dynload_dir}/_tkinter.so

%files test
%defattr(-, root, root, -)
%{pylibdir}/bsddb/test
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/email/test
%{pylibdir}/json/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test/*
%exclude %{pylibdir}/test/test_support.py*
%exclude %{pylibdir}/test/__init__.py*
%{dynload_dir}/_ctypes_test.so
%{dynload_dir}/_testcapi.so

%changelog
