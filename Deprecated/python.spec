# ======================================================
# Conditionals and other variables controlling the build
# ======================================================
%global run_selftest_suite 0
%global with_rewheel 1

#%{!?__python_ver:%global __python_ver EMPTY}
%global __python_ver 27
%global unicode ucs4

%if "%{__python_ver}" != "EMPTY"
%global main_python 0
%global python python%{__python_ver}
%global tkinter tkinter%{__python_ver}
%else
%global main_python 1
%global python python
%global tkinter tkinter
%endif

%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global tools_dir %{pylibdir}/Tools
%global demo_dir %{pylibdir}/Demo
%global doc_tools_dir %{pylibdir}/Doc/tools
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{pybasever}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug     libpython%{pybasever}_d.so.%{py_SOVERSION}

%global with_debug_build 1
%global with_huntrleaks 0
%global with_gdb_hooks 1
%global with_systemtap 1
%ifnarch s390
%global with_valgrind 1
%else
%global with_valgrind 0
%endif
%global with_gdbm 1
%global _python_bytecompile_errors_terminate_build 0
%global regenerate_autotooling_patch 0



Summary: An interpreted, interactive, object-oriented programming language
Name: %{python}
Version: 2.7.11
Release: 4.%{?dist}
License: Python
Group: Development/Languages
Requires: %{python}-libs%{?_isa} = %{version}-%{release}
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
Provides: python27(dist-packages)
Provides: python27(alternatives)
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: expat-devel >= 2.1.0
BuildRequires: findutils
#BuildRequires: gcc-c++
%if %{with_gdbm}
BuildRequires: gdbm-devel
%endif
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
%global tapsetdir      /usr/share/systemtap/tapset
%endif # with_systemtap
BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel
%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif
BuildRequires: zlib-devel
%if 0%{?with_rewheel}
BuildRequires: %{python}-setuptools
BuildRequires: %{python}-pip
Requires: %{python}-setuptools
Requires: %{python}-pip
%endif

Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source2: pythondeps.sh
%global __python_requires %{SOURCE2}
Source3: libpython.stp
Source4: systemtap-example.stp
Source5: pyfuntop.stp
Source7: pynche
Source8: macros.python27
Source9: macros.python27_build

Patch0: python-2.7.1-config.patch
Patch1: 00001-pydocnogui.patch
Patch4: python-2.5-cflags.patch
Patch6: python-2.5.1-plural-fix.patch
Patch7: python-2.5.1-sqlite-encoding.patch
Patch10: python-2.7rc1-binutils-no-dep.patch
Patch13: python-2.7rc1-socketmodule-constants.patch
Patch14: python-2.7rc1-socketmodule-constants2.patch
Patch16: python-2.6-rpath.patch
Patch17: python-2.6.4-distutils-rpath.patch
Patch55: 00055-systemtap.patch
Patch102: python-2.7.3-lib64.patch
Patch103: python-2.7-lib64-sysconfig.patch
Patch104: 00104-lib64-fix-for-test_install.patch
Patch111: 00111-no-static-lib.patch
Patch112: python-2.7.3-debug-build.patch
Patch113: 00113-more-configuration-flags.patch
Patch114: 00114-statvfs-f_flag-constants.patch
Patch121: 00121-add-Modules-to-build-path.patch
Patch125: 00125-less-verbose-COUNT_ALLOCS.patch
Patch128: python-2.7.1-fix_test_abc_with_COUNT_ALLOCS.patch
Patch130: python-2.7.2-add-extension-suffix-to-python-config.patch
Patch131: 00131-disable-tests-in-test_io.patch
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch
Patch133: 00133-skip-test_dl.patch
Patch134: 00134-fix-COUNT_ALLOCS-failure-in-test_sys.patch
Patch135: 00135-skip-test-within-test_weakref-in-debug-build.patch
Patch136: 00136-skip-tests-of-seeking-stdin-in-rpmbuild.patch
Patch137: 00137-skip-distutils-tests-that-fail-in-rpmbuild.patch
Patch138: 00138-fix-distutils-tests-in-debug-build.patch
Patch139: 00139-skip-test_float-known-failure-on-arm.patch
Patch140: 00140-skip-test_ctypes-known-failure-on-sparc.patch
Patch141: 00141-fix-test_gc_with_COUNT_ALLOCS.patch
Patch142: 00142-skip-failing-pty-tests-in-rpmbuild.patch
Patch143: 00143-tsc-on-ppc.patch
Patch144: 00144-no-gdbm.patch
Patch146: 00146-hashlib-fips.patch
Patch147: 00147-add-debug-malloc-stats.patch
Patch153: 00153-fix-test_gdb-noise.patch
Patch155: 00155-avoid-ctypes-thunks.patch
Patch156: 00156-gdb-autoload-safepath.patch
Patch157: 00157-uid-gid-overflows.patch
Patch165: 00165-crypt-module-salt-backport.patch
Patch166: 00166-fix-fake-repr-in-gdb-hooks.patch
Patch167: 00167-disable-stack-navigation-tests-when-optimized-in-test_gdb.patch
Patch168: 00168-distutils-cflags.patch
Patch169: 00169-avoid-implicit-usage-of-md5-in-multiprocessing.patch
Patch170: 00170-gc-assertions.patch
Patch173: 00173-workaround-ENOPROTOOPT-in-bind_port.patch
Patch174: 00174-fix-for-usr-move.patch
Patch180: 00180-python-add-support-for-ppc64p7.patch
Patch181: 00181-allow-arbitrary-timeout-in-condition-wait.patch
Patch184: 00184-ctypes-should-build-with-libffi-multilib-wrapper.patch
Patch185: 00185-urllib2-honors-noproxy-for-ftp.patch
Patch187: 00187-add-RPATH-to-pyexpat.patch
Patch189: 00189-gdb-py-bt-dont-raise-exception-from-eval.patch
Patch191: 00191-disable-NOOP.patch
Patch193: 00193-enable-loading-sqlite-extensions.patch
%if 0%{with_rewheel}
Patch198: 00198-add-rewheel-module.patch
%endif
Patch200: 00200-skip-thread-test.patch
Patch5000: 05000-autotool-intermediates.patch
%if %{main_python}
Obsoletes: Distutils
Provides: Distutils
Obsoletes: python2
Provides: python2 = %{version}
Obsoletes: python-elementtree <= 1.2.6
Obsoletes: python-ordereddict <= 1.1-8
Obsoletes: python-sqlite < 2.3.2
Provides: python-sqlite = 2.3.2
Obsoletes: python-ctypes < 1.0.1
Provides: python-ctypes = 1.0.1
Obsoletes: python-hashlib < 20081120
Provides: python-hashlib = 20081120
Obsoletes: python-uuid < 1.31
Provides: python-uuid = 1.31
Obsoletes: PyXML <= 0.8.4-29
Provides:   python-argparse = %{version}-%{release}
%endif

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
Requires: expat >= 2.1.0

%description libs
This package contains runtime libraries for use by Python:
- the libpython dynamic library, for use by applications that embed Python as
a scripting language, and by the main "python" executable
- the Python standard library

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{python}%{?_isa} = %{version}-%{release}
#Requires: python-rpm-macros
#Requires: python2-rpm-macros
Requires: pkgconfig
Conflicts: %{python} < %{version}-%{release}
%if %{main_python}
Obsoletes: python2-devel
Provides: python2-devel = %{version}-%{release}
Provides: python2-devel%{?_isa} = %{version}-%{release}
%endif

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
%if %{main_python}
Obsoletes: python2-tools
Provides: python2-tools = %{version}
%endif

%description tools
This package includes several tools to help with the development of Python
programs, including IDLE (an IDE with editing and debugging facilities), a
color editor (pynche), and a python gettext program (pygettext.py).

%package -n %{tkinter}
Summary: A graphical user interface for the Python scripting language
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
%if %{main_python}
Obsoletes: tkinter2
Provides: tkinter2 = %{version}
%endif

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

%if 0%{?with_debug_build}
%package debug
Summary: Debug version of the Python runtime
Group: Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: tkinter%{?_isa} = %{version}-%{release}
Requires: %{name}-tools%{?_isa} = %{version}-%{release}

%description debug
python-debug provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users, such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python build,
but is useful for tracking down reference-counting issues, and other bugs.

The bytecodes are unchanged, so that .pyc files are compatible between the two
version of Python, but the debugging features mean that C/C++ extension modules
are ABI-incompatible with those built for the standard runtime.

It shares installation directories with the standard Python runtime, so that
.py and .pyc files can be shared.  All compiled extension modules gain a "_d"
suffix ("foo_d.so" rather than "foo.so") so that each Python implementation can
load its own extensions.
%endif

%prep
%setup -q -n Python-%{version}

%if 0%{?with_systemtap}
cp -a %{SOURCE4} .
cp -a %{SOURCE5} .
%endif # with_systemtap
rm -r Modules/expat || exit 1
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done
rm -r Modules/zlib || exit 1
for f in md5module.c md5.c shamodule.c sha256module.c sha512module.c; do
    rm Modules/$f
done
%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .no_gui
%patch4 -p1 -b .cflags
%patch6 -p1 -b .plural
%patch7 -p1
%if "%{_lib}" == "lib64"
%patch102 -p1 -b .lib64
%patch103 -p1 -b .lib64-sysconfig
%patch104 -p1
%endif
%patch10 -p1 -b .binutils-no-dep
# patch11: upstream as of Python 2.7.3
%patch13 -p1 -b .socketmodule
%patch14 -p1 -b .socketmodule2
%patch16 -p1 -b .rpath
%patch17 -p1 -b .distutils-rpath
%if 0%{?with_systemtap}
%patch55 -p1 -b .systemtap
%endif
%patch111 -p1 -b .no-static-lib
%patch112 -p1 -b .debug-build
%patch113 -p1 -b .more-configuration-flags
%patch114 -p1 -b .statvfs-f-flag-constants
%patch121 -p1
%patch125 -p1 -b .less-verbose-COUNT_ALLOCS
%patch128 -p1
%patch130 -p1
%ifarch ppc %{power64}
%patch131 -p1
%endif
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1 -b .stdin-test
%patch137 -p1
%patch138 -p1
%ifarch %{arm}
%patch139 -p1
%endif
%ifarch %{sparc}
%patch140 -p1
%endif
%patch141 -p1
%patch142 -p1 -b .tty-fail
%patch143 -p1 -b .tsc-on-ppc
%if !%{with_gdbm}
%patch144 -p1
%endif
%patch146 -p1
%patch147 -p1
%patch153 -p0
%patch155 -p1
%patch156 -p1
%patch157 -p1
%patch165 -p1
mv Modules/cryptmodule.c Modules/_cryptmodule.c
%patch166 -p1
%patch167 -p1
%patch168 -p1
%patch169 -p1
%patch170 -p1
%patch173 -p1
%patch174 -p1 -b .fix-for-usr-move
%patch180 -p1
%patch181 -p1
%patch184 -p1
%patch185 -p1
%patch187 -p1
%patch189 -p1
%patch191 -p1
%patch193 -p1
%if 0%{with_rewheel}
%patch198 -p1
%endif
%patch200 -p1
find -name "*~" |xargs rm -f
%if ! 0%{regenerate_autotooling_patch}
%patch5000 -p0 -b .autotool-intermediates
%endif
%build
topdir=$(pwd)
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
export LDFLAGS="$RPM_LD_FLAGS"
if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
  export LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi
export CC=gcc

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
  %global _configure $topdir/configure

%configure \
  --prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --sysconfdir=/etc \
  --includedir=%{_includedir} \
  --enable-profiling \
  --with-threads \
  --with-pth \
  --with-ensurepip="upgrade" \
  --enable-ipv6 \
  --enable-shared \
  --enable-unicode=%{unicode} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
%if 0%{?with_systemtap}
  --with-dtrace \
  --with-tapset-install-dir=%{tapsetdir} \
%endif
%if 0%{?with_valgrind}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

make EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}
if $PathFixWithThisBinary
then
  LD_LIBRARY_PATH="$topdir/$ConfDir" ./$BinaryName \
    $topdir/Tools/scripts/pathfix.py \
      -i "/usr/bin/env $BinaryName" \
      $topdir
fi
ln -s $BinaryName $SymlinkName
LD_LIBRARY_PATH="$topdir/$ConfDir" PATH=$PATH:$topdir/$ConfDir make -s EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}

  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfDir
}
%if 0%{?with_debug_build}
BuildPython debug \
  python-debug \
  python%{pybasever}-debug \
%ifarch %{ix86} x86_64 ppc %{power64}
  "--with-pydebug --with-tsc --with-count-allocs --with-call-profile" \
%else
  "--with-pydebug --with-count-allocs --with-call-profile" \
%endif
  false
%endif

BuildPython optimized \
  python \
  python%{pybasever} \
  "" \
  true
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
%if 0%{?with_gdb_hooks}
DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName.debug-gdb.py
mkdir -p %{buildroot}$DirHoldingGdbPy
cp $topdir/Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName \
  -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"

LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName -O \
  -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"
%endif
  popd
  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}
%if 0%{?with_debug_build}
InstallPython debug \
  python%{pybasever}-debug \
  %{py_INSTSONAME_debug}
%endif
InstallPython optimized \
  python%{pybasever} \
  %{py_INSTSONAME_optimized}
for fixed in %{buildroot}%{_bindir}/pydoc; do
    sed 's,#!.*/python$,#!/usr/bin/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
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

%if %{main_python}
%else
mv %{buildroot}%{_bindir}/python %{buildroot}%{_bindir}/%{python}
%if 0%{?with_debug_build}
mv %{buildroot}%{_bindir}/python-debug %{buildroot}%{_bindir}/%{python}-debug
%endif
#mv %{buildroot}/%{_mandir}/man1/python.1 %{buildroot}/%{_mandir}/man1/python%{pybasever}.1
%endif
mkdir -p ${RPM_BUILD_ROOT}%{site_packages}
install -p -m755 %{SOURCE7} ${RPM_BUILD_ROOT}%{_bindir}/pynche
/bin/chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/pynche
rm -f Tools/pynche/*.pyw
cp -rp Tools/pynche \
  ${RPM_BUILD_ROOT}%{site_packages}/
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
rm -f %{buildroot}%{pylibdir}/LICENSE.txt
%if !%{main_python}
pushd %{buildroot}%{_bindir}
mv idle idle%{__python_ver}
mv pynche pynche%{__python_ver}
mv pygettext.py pygettext%{__python_ver}.py
mv msgfmt.py msgfmt%{__python_ver}.py
mv smtpd.py smtpd%{__python_ver}.py
mv pydoc pydoc%{__python_ver}
popd
%endif
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au
%if "%{_lib}" == "lib64"
install -d %{buildroot}/%{_prefix}/lib/python%{pybasever}/site-packages
%endif
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h
%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64
%global _pyconfig_h %{_pyconfig64_h}
%else
%global _pyconfig_h %{_pyconfig32_h}
%endif
%if 0%{?with_debug_build}
%global PyIncludeDirs python%{pybasever} python%{pybasever}-debug
%else
%global PyIncludeDirs python%{pybasever}
%endif
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
ln -s ../../libpython%{pybasever}.so %{buildroot}%{pylibdir}/config/libpython%{pybasever}.so
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/rpm/macros.python
install -m 644 %{SOURCE9} %{buildroot}%{_rpmconfigdir}/macros.d/macros.python
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
%if 0%{?with_systemtap}
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64
%global libpython_stp_optimized libpython%{pybasever}-64.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-64.stp
%else
%global libpython_stp_optimized libpython%{pybasever}-32.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-32.stp
%endif

sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_optimized}|" \
   %{SOURCE3} \
   > %{buildroot}%{tapsetdir}/%{libpython_stp_optimized}

%if 0%{?with_debug_build}
sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_debug}|" \
   %{SOURCE3} \
   > %{buildroot}%{tapsetdir}/%{libpython_stp_debug}
%endif
%endif
/bin/chmod 755 %{buildroot}%{dynload_dir}/*.so
/bin/chmod 755 %{buildroot}%{_libdir}/libpython%{pybasever}.so.1.0
/bin/chmod 755 %{buildroot}%{_libdir}/libpython%{pybasever}_d.so.1.0
ITEMS="
/usr/lib/python2.7/site-packages/setuptools*
/usr/lib/python2.7/site-packages/pip*
/usr/lib/python2.7/site-packages/pkg_resources/*
%{_bindir}/easy_install*
%{_bindir}/pip*
%{_bindir}/python-config
%{_bindir}/python-debug-config
%{_bindir}/python2
%{_bindir}/python2-config
%{_bindir}/python2-debug
%{_bindir}/python2-debug-config
/usr/lib/python2.7/site-packages/_markerlib*
/usr/lib/python2.7/site-packages/easy_install*
"
for i in $ITEMS;do
    rm -rf %{buildroot}$i
done

%clean
rm -fr %{buildroot}
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%{_bindir}/pydoc*
%{_bindir}/%{python}
%if %{main_python}
%{_bindir}/python2
%endif
%{_bindir}/python%{pybasever}
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/Python-%{version}-py%{pybasever}.egg-info
%{dynload_dir}/_bisectmodule.so
%{dynload_dir}/_bsddb.so
%{dynload_dir}/_codecs_cn.so
%{dynload_dir}/_codecs_hk.so
%{dynload_dir}/_codecs_iso2022.so
%{dynload_dir}/_codecs_jp.so
%{dynload_dir}/_codecs_kr.so
%{dynload_dir}/_codecs_tw.so
%{dynload_dir}/_collectionsmodule.so
%{dynload_dir}/_csv.so
%{dynload_dir}/_ctypes.so
%{dynload_dir}/_curses.so
%{dynload_dir}/_curses_panel.so
%{dynload_dir}/_elementtree.so
%{dynload_dir}/_functoolsmodule.so
%{dynload_dir}/_hashlib.so
%{dynload_dir}/_heapq.so
%{dynload_dir}/_hotshot.so
%{dynload_dir}/_io.so
%{dynload_dir}/_json.so
%{dynload_dir}/_localemodule.so
%{dynload_dir}/_lsprof.so
%{dynload_dir}/_multibytecodecmodule.so
%{dynload_dir}/_multiprocessing.so
%{dynload_dir}/_randommodule.so
%{dynload_dir}/_socketmodule.so
%{dynload_dir}/_sqlite3.so
%{dynload_dir}/_ssl.so
%{dynload_dir}/_struct.so
%{dynload_dir}/arraymodule.so
%{dynload_dir}/audioop.so
%{dynload_dir}/binascii.so
%{dynload_dir}/bz2.so
%{dynload_dir}/cPickle.so
%{dynload_dir}/cStringIO.so
%{dynload_dir}/cmathmodule.so
%{dynload_dir}/_cryptmodule.so
%{dynload_dir}/datetime.so
%{dynload_dir}/dbm.so
%{dynload_dir}/dlmodule.so
%{dynload_dir}/fcntlmodule.so
%{dynload_dir}/future_builtins.so
%if %{with_gdbm}
%{dynload_dir}/gdbmmodule.so
%endif
%{dynload_dir}/grpmodule.so
%{dynload_dir}/imageop.so
%{dynload_dir}/itertoolsmodule.so
%{dynload_dir}/linuxaudiodev.so
%{dynload_dir}/math.so
%{dynload_dir}/mmapmodule.so
%{dynload_dir}/nismodule.so
%{dynload_dir}/operator.so
%{dynload_dir}/ossaudiodev.so
%{dynload_dir}/parsermodule.so
%{dynload_dir}/pyexpat.so
%{dynload_dir}/readline.so
%{dynload_dir}/resource.so
%{dynload_dir}/selectmodule.so
%{dynload_dir}/spwdmodule.so
%{dynload_dir}/stropmodule.so
%{dynload_dir}/syslog.so
%{dynload_dir}/termios.so
%{dynload_dir}/timemodule.so
%{dynload_dir}/timingmodule.so
%{dynload_dir}/unicodedata.so
%{dynload_dir}/xxsubtype.so
%{dynload_dir}/zlibmodule.so

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
%exclude %{pylibdir}/lib2to3/tests
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

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the libs
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config
%{pylibdir}/config/Makefile
%dir %{_includedir}/python%{pybasever}
%{_includedir}/python%{pybasever}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}
%if 0%{?with_systemtap}
%dir %(dirname %{tapsetdir})
%dir %{tapsetdir}
%{tapsetdir}/%{libpython_stp_optimized}
%doc systemtap-example.stp pyfuntop.stp
%endif

%dir %{pylibdir}/ensurepip/
%{pylibdir}/ensurepip/*.py*
%exclude %{pylibdir}/ensurepip/_bundled

%if 0%{?with_rewheel}
%dir %{pylibdir}/ensurepip/rewheel/
%{pylibdir}/ensurepip/rewheel/*.py*
%endif
%if 0%{?with_debug_build}
%{_usr}/lib/debug%{_libdir}/libpython2.7.so.1.0.debug-gdb.*
%{_usr}/lib/debug%{_libdir}/libpython2.7_d.so.1.0.debug-gdb.*
%endif

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
%if %{main_python}
%{_bindir}/python-config
%{_bindir}/python2-config
%endif
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
%{pylibdir}/lib2to3/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test/*
# These two are shipped in the main subpackage:
%exclude %{pylibdir}/test/test_support.py*
%exclude %{pylibdir}/test/__init__.py*
%{dynload_dir}/_ctypes_test.so
%{dynload_dir}/_testcapimodule.so


# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if 0%{?with_debug_build}
%files debug
%defattr(-,root,root,-)

# Analog of the core subpackage's files:
%{_bindir}/%{python}-debug
%if %{main_python}
%{_bindir}/python2-debug
%endif
%{_bindir}/python%{pybasever}-debug

# Analog of the -libs subpackage's files, with debug builds of the built-in
# "extension" modules:
%{dynload_dir}/_bisectmodule_d.so
%{dynload_dir}/_bsddb_d.so
%{dynload_dir}/_codecs_cn_d.so
%{dynload_dir}/_codecs_hk_d.so
%{dynload_dir}/_codecs_iso2022_d.so
%{dynload_dir}/_codecs_jp_d.so
%{dynload_dir}/_codecs_kr_d.so
%{dynload_dir}/_codecs_tw_d.so
%{dynload_dir}/_collectionsmodule_d.so
%{dynload_dir}/_csv_d.so
%{dynload_dir}/_ctypes_d.so
%{dynload_dir}/_curses_d.so
%{dynload_dir}/_curses_panel_d.so
%{dynload_dir}/_elementtree_d.so
%{dynload_dir}/_functoolsmodule_d.so
%{dynload_dir}/_hashlib_d.so
%{dynload_dir}/_heapq_d.so
%{dynload_dir}/_hotshot_d.so
%{dynload_dir}/_io_d.so
%{dynload_dir}/_json_d.so
%{dynload_dir}/_localemodule_d.so
%{dynload_dir}/_lsprof_d.so
%{dynload_dir}/_multibytecodecmodule_d.so
%{dynload_dir}/_multiprocessing_d.so
%{dynload_dir}/_randommodule_d.so
%{dynload_dir}/_socketmodule_d.so
%{dynload_dir}/_sqlite3_d.so
%{dynload_dir}/_ssl_d.so
%{dynload_dir}/_struct_d.so
%{dynload_dir}/arraymodule_d.so
%{dynload_dir}/audioop_d.so
%{dynload_dir}/binascii_d.so
%{dynload_dir}/bz2_d.so
%{dynload_dir}/cPickle_d.so
%{dynload_dir}/cStringIO_d.so
%{dynload_dir}/cmathmodule_d.so
%{dynload_dir}/_cryptmodule_d.so
%{dynload_dir}/datetime_d.so
%{dynload_dir}/dbm_d.so
%{dynload_dir}/dlmodule_d.so
%{dynload_dir}/fcntlmodule_d.so
%{dynload_dir}/future_builtins_d.so
%if %{with_gdbm}
%{dynload_dir}/gdbmmodule_d.so
%endif
%{dynload_dir}/grpmodule_d.so
%{dynload_dir}/imageop_d.so
%{dynload_dir}/itertoolsmodule_d.so
%{dynload_dir}/linuxaudiodev_d.so
%{dynload_dir}/math_d.so
%{dynload_dir}/mmapmodule_d.so
%{dynload_dir}/nismodule_d.so
%{dynload_dir}/operator_d.so
%{dynload_dir}/ossaudiodev_d.so
%{dynload_dir}/parsermodule_d.so
%{dynload_dir}/pyexpat_d.so
%{dynload_dir}/readline_d.so
%{dynload_dir}/resource_d.so
%{dynload_dir}/selectmodule_d.so
%{dynload_dir}/spwdmodule_d.so
%{dynload_dir}/stropmodule_d.so
%{dynload_dir}/syslog_d.so
%{dynload_dir}/termios_d.so
%{dynload_dir}/timemodule_d.so
%{dynload_dir}/timingmodule_d.so
%{dynload_dir}/unicodedata_d.so
%{dynload_dir}/xxsubtype_d.so
%{dynload_dir}/zlibmodule_d.so

# No need to split things out the "Makefile" and the config-32/64.h file as we
# do for the regular build above (bug 531901), since they're all in one package
# now; they're listed below, under "-devel":

%{_libdir}/%{py_INSTSONAME_debug}
%if 0%{?with_systemtap}
%dir %(dirname %{tapsetdir})
%dir %{tapsetdir}
%{tapsetdir}/%{libpython_stp_debug}
%endif

# Analog of the -devel subpackage's files:
%dir %{pylibdir}/config-debug
%{_libdir}/pkgconfig/python-%{pybasever}-debug.pc
%{_libdir}/pkgconfig/python-debug.pc
%{_libdir}/pkgconfig/python2-debug.pc
%{pylibdir}/config-debug/*
%{_includedir}/python%{pybasever}-debug/*.h
%if %{main_python}
%{_bindir}/python-debug-config
%{_bindir}/python2-debug-config
%endif
%{_bindir}/python%{pybasever}-debug-config
%{_libdir}/libpython%{pybasever}_d.so

# Analog of the -tools subpackage's files:
#  None for now; we could build precanned versions that have the appropriate
# shebang if needed

# Analog  of the tkinter subpackage's files:
%{dynload_dir}/_tkinter_d.so

# Analog  of the -test subpackage's files:
%{dynload_dir}/_ctypes_test_d.so
%{dynload_dir}/_testcapimodule_d.so

%endif # with_debug_build

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from
# ldconfig (rhbz:562980).
#
# The /usr/lib/rpm/redhat/macros defines the __debug_package macro to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
#
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py
# payload file would be unpackaged)


# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
