%define snap 20150325

Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.1
Release:	1.%{snap}cvs.%{dist}
License:	BSD
Vendor: %{vendor}
Packager: %{packager}
Group:		System Environment/Libraries
URL:		http://www.thrysoee.dk/editline/
Source0:	http://www.thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 	gawk
BuildRequires: 	ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD Editline library.
It provides generic line editing, history, and tokenization functions, similar
to those found in GNU Readline.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	ncurses-devel

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n %{name}-%{snap}-%{version}

# Suppress rpmlint error.
iconv --from-code ISO8859-1 --to-code UTF-8 ./ChangeLog \
  --output ChangeLog.utf-8 && mv ChangeLog.utf-8 ./ChangeLog

%build
%configure --disable-static

# Trying to omit unused direct shared library dependencies leads to
# undefined non-weak symbols.

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING THANKS
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/fileman.c 
%doc %{_mandir}/man3/*
%doc %{_mandir}/man5/editrc.5*
%{_includedir}/histedit.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%dir %{_includedir}/editline
%{_includedir}/editline/readline.h

%changelog
