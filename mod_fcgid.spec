%global selinux_module 0
%global selinux_types %{nil}
%global selinux_variants %{nil}
%global selinux_buildreqs %{nil}
%define opt_apache /opt/apache2.2

%global rundir %{_localstatedir}/run

Name:		mod_fcgid
Version:	2.3.9
Release:	1.%{dist}
Summary:	FastCGI interface module for Apache
Group:		System Environment/Daemons
License:	ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
URL:		http://httpd.apache.org/mod_fcgid/
Source0:	http://www.apache.org/dist/httpd/mod_fcgid/mod_fcgid-%{version}.tar.bz2
Source1:	fcgid.conf
Source2:	mod_fcgid-2.1-README.RPM
Source3:	mod_fcgid-2.1-README.SELinux
Source4:	mod_fcgid-tmpfs.conf
Source5:	fcgid24.conf
Source10:	fastcgi.te
Source11:	fastcgi-2.5.te
Source12:	fastcgi.fc
Patch0:		mod_fcgid-2.3.4-fixconf-shellbang.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	httpd, httpd-devel, httpd-tools, pkgconfig
Requires:	httpd
# sed required for fixconf script
Requires:	/bin/sed
Conflicts:	selinux-policy < 2.4.6-279.el5
# No provide here because selinux-policy >= 2.4.6-279.el5 does the providing
Obsoletes:	mod_fcgid-selinux <= %{version}-%{release}

%description
mod_fcgid is a binary-compatible alternative to the Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on reducing
the number of fastcgi servers, and kicking out corrupt fastcgi servers as soon
as possible.


%prep
%setup -q
cp -p %{SOURCE1} fcgid.conf
cp -p %{SOURCE2} README.RPM
cp -p %{SOURCE3} README.SELinux
cp -p %{SOURCE5} fcgid24.conf
%if 0%{?selinux_policynum} < 20501
cp -p %{SOURCE10} fastcgi.te
%else
cp -p %{SOURCE11} fastcgi.te
%endif
cp -p %{SOURCE12} fastcgi.fc

# Fix shellbang in fixconf script for our location of sed
%patch0 -p1

%build
APXS=%{opt_apache}/bin/apxs ./configure.apxs
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} MKINSTALLDIRS="mkdir -p" install
mkdir -p %{buildroot}%{opt_apache}/conf
echo "LoadModule fcgid_module modules/mod_fcgid.so" > %{buildroot}%{opt_apache}/conf/fcgid.conf
install -D -m 644 fcgid.conf %{buildroot}%{opt_apache}/conf/fcgid.conf
install -d -m 755 %{buildroot}%{rundir}/mod_fcgid


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
# mod_fcgid.html.en is explicitly encoded as ISO-8859-1
%doc CHANGES-FCGID LICENSE-FCGID NOTICE-FCGID README-FCGID STATUS-FCGID
%doc %{opt_apache}/manual/mod/mod_fcgid.html
%doc %{opt_apache}/manual/mod/mod_fcgid.html.en
%doc %{opt_apache}/manual/mod/mod_fcgid.xml.meta
%doc %{opt_apache}/manual/mod/mod_fcgid.xml
%doc build/fixconf.sed
%{opt_apache}/modules/mod_fcgid.so
%config(noreplace) %{opt_apache}/conf/fcgid.conf
%dir %attr(0755,apache,www) %{rundir}/mod_fcgid/


%changelog
