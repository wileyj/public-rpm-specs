%define repo https://github.com/open-source-parsers/jsoncpp
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1


%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

Name:       jsoncpp
Version:    %{gitversion}
Release:    %{rel_version}.%{revision}.%{dist}
Summary:    JSON library implemented in C++
Group:      System Environment/Libraries
License:    Public Domain or MIT
URL:        https://github.com/open-source-parsers/jsoncpp
Source0:    %{name}.tar.gz

BuildRequires:  cmake doxygen graphviz

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.


%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
grep -e "-Wall" SConstruct
sed 's|CCFLAGS = "-Wall"|CCFLAGS = "%{optflags}"|' -i SConstruct

%build
cd %{name}-%{version}
#scons platform=linux-gcc %{?_smp_mflags}
mkdir -p build/release
cd build/release
cmake -DCMAKE_BUILD_TYPE=release -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=ON -DARCHIVE_INSTALL_DIR=%{buildroot} -G "Unix Makefiles" ../..
make


# Now, lets make a proper shared lib. :P
#g++ -o libjsoncpp.so.0.0.0 -shared -Wl,-z,now -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread

# Build the doc
cd ../..
%{python} doxybuild.py --with-dot --doxygen %{_bindir}/doxygen

#%check
#scons platform=linux-gcc check %{?_smp_mflags}

%install
cd %{name}-%{version}/build/release
make DESTDIR=%{buildroot} INSTALL="install -p" install
cd  ../..
mv %{buildroot}/usr/local/lib64 %{buildroot}%{_libdir}
mv %{buildroot}/usr/local/include %{buildroot}%{_includedir}
rm -rf %{buildroot}/opt
rm -rf %{buildroot}/usr/local

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html
for f in AUTHORS LICENSE NEWS.txt README.md ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html
sed -i 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/jsoncpp.pc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%{_docdir}/%{name}/
%{_libdir}/lib%{name}*

%files devel
#%{_libdir}/lib%{name}.so
%dir %{_includedir}/json
%{_includedir}/json/*
%{_libdir}/pkgconfig/jsoncpp.pc

%files doc
%{_docdir}/%{name}/

