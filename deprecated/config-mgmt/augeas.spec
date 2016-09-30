%define repo https://github.com/hercules-team/augeas
Name:           augeas
Version:        1.4.0
Release:        1.%{dist}
Summary:        A library for changing configuration files
Group:          System Environment/Libraries
License:        LGPLv2+
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            http://augeas.net/
#Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  readline-devel libselinux-devel libxml2-devel
Requires:       %{name}-libs = %{version}-%{release}

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description    libs
The libraries for %{name}.

Augeas is a library for programmatically editing configuration files. It parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
#git clone git://git.savannah.gnu.org/gnulib.git

%build
cd %{name}-%{version}
./autogen.sh

%configure --disable-static
make %{?_smp_mflags}

%install
cd %{name}-%{version}

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -r $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/dist/tests

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/fadot
%doc %{_mandir}/man1/*
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%defattr(-,root,root,-)
%{_datadir}/augeas/lenses/dist
%{_libdir}/*.so.*
#%doc AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%changelog
