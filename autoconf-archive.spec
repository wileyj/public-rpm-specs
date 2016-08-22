Name: autoconf-archive
Version: 2014.10.15
Release: 1.%{dist}
Summary: The Autoconf Macro Archive
Group: Development/Tools
License: GPLv3+ with exceptions
Vendor: %{vendor}
Packager: %{packager}
URL: http://www.gnu.org/software/autoconf-archive/
Source0: ftp://ftp.gnu.org/gnu/autoconf-archive/%{name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: autoconf
BuildRequires: xz
Requires(post): info
Requires(preun): info

%description
The GNU Autoconf Archive is a collection of more than 450 macros for
GNU Autoconf that have been contributed as free software by friendly
supporters of the cause from all over the Internet.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# remove dir file which will be generated by /sbin/install-info
rm -f %{buildroot}%{_infodir}/dir
# document files are installed another location
rm -rf %{buildroot}%{_datadir}/%{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog NEWS README TODO
%{_datadir}/aclocal/*.m4
%{_infodir}/autoconf-archive.info*

%changelog
