Name:       jsoncpp
Version:    0.10.5
Release:    1.%{dist}
Summary:    JSON library implemented in C++
Group:      System Environment/Libraries
License:    Public Domain or MIT
URL:        https://github.com/open-source-parsers/jsoncpp
Source0:    %{name}.tar.gz
Source1:    jsoncpp.pc

BuildRequires:  python scons doxygen
BuildRequires:  graphviz

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
%setup -q -n %{name}
grep -e "-Wall" SConstruct
sed 's|CCFLAGS = "-Wall"|CCFLAGS = "%{optflags}"|' -i SConstruct

%build
git pull
scons platform=linux-gcc %{?_smp_mflags}
# Now, lets make a proper shared lib. :P
g++ -o libjsoncpp.so.0.0.0 -shared -Wl,-z,now -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread
# Build the doc
python doxybuild.py --with-dot --doxygen %{_bindir}/doxygen

%check
scons platform=linux-gcc check %{?_smp_mflags}

%install
install -p -D lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0.0.0
ln -s %{_libdir}/lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
ln -s %{_libdir}/lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/json
install -p -m 0644 include/json/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/json
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html
for f in AUTHORS LICENSE NEWS.txt README.md ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html
install -d $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
sed -i 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/jsoncpp.pc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_docdir}/%{name}/
%exclude %{_docdir}/%{name}/html
%{_libdir}/lib%{name}.so.0
%{_libdir}/lib%{name}.so.0.0.0

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/jsoncpp.pc

%files doc
%{_docdir}/%{name}/

