%define _sbindir /sbin

Name:           runit
Version:        2.1.1
Release:        1.%{dist}
Group:          System/Base
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Url:            http://smarden.org/runit/
Source:         http://smarden.org/runit/runit-%{version}.tar.gz
Patch:          runit-2.1.1-etc-service.patch
Patch1:         runit-2.1.1-runsvdir-path-cleanup.patch
Patch2:         runit-2.1.1-term-hup-option.patch
Obsoletes: runit <= %{version}-%{release}
Provides: runit = %{version}-%{release}
BuildRequires: make gcc
BuildRequires:        glibc-static
%{?_with_dietlibc:BuildRequires:        dietlibc}

Summary:        A UNIX init scheme with service supervision

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems. runit implements a simple three-stage concept. Stage 1 performs the
system's one-time initialization tasks. Stage 2 starts the system's uptime
services (via the runsvdir program). Stage 3 handles the tasks necessary to
shutdown and halt or reboot.

Authors:
---------
    Gerrit Pape <pape@smarden.org>

%prep
%setup -q -n admin/%{name}-%{version}
pushd src
echo "%{?_with_dietlibc:diet -Os }%__cc $RPM_OPT_FLAGS" >conf-cc
echo "%{?_with_dietlibc:diet -Os }%__cc -Os -pipe"      >conf-ld
popd
%patch
%patch1
%patch2
  	sed -i -e "s|^char\ \*varservice\ \=\"/service/\";$|char\ \*varservice\ \=\"' + service_path + '/\";|" src/sv.c
  	sed -i -e s:-static:: src/Makefile

%build
sh package/compile

%install
for i in $(< package/commands) ; do
    %{__install} -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    %{__install} -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done
%{__install} -d -m 0755 %{buildroot}/etc/service
%{__install} -D -m 0750 etc/2 %{buildroot}%{_sbindir}/runsvdir-start


%post
if [ $1 = 1 ] ; then
  rpm --queryformat='%%{name}' -qf /sbin/init | grep -q upstart
  if [ $? -eq 0 ]
  then
    cat >/etc/init/runsvdir.conf <<\EOT
# for runit - manage /usr/sbin/runsvdir-start
start on runlevel [2345]
stop on runlevel [^2345]
normal exit 0 111
respawn
exec /sbin/runsvdir-start
EOT
    # tell init to start the new service
    start runsvdir
  else
    grep -q 'RI:2345:respawn:/sbin/runsvdir-start' /etc/inittab
    if [ $? -eq 1 ]
    then
      echo -n "Installing /sbin/runsvdir-start into /etc/inittab.."
      echo "RI:2345:respawn:/sbin/runsvdir-start" >> /etc/inittab
      echo " success."
      # Reload init
      telinit q
    fi
  fi
fi

%preun
if [ $1 = 0 ]
then
  if [ -f /etc/init/runsvdir.conf ]
  then
    stop runsvdir
  fi
fi

%postun
if [ $1 = 0 ]
then
  if [ -f /etc/init/runsvdir.conf ]
  then
    rm -f /etc/init/runsvdir.conf
  else
    echo " #################################################"
    echo " # Remove /sbin/runsvdir-start from /etc/inittab #"
    echo " # if you really want to remove runit            #"
    echo " #################################################"
  fi
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_sbindir}/chpst
%{_sbindir}/runit
%{_sbindir}/runit-init
%{_sbindir}/runsv
%{_sbindir}/runsvchdir
%{_sbindir}/runsvdir
%{_sbindir}/sv
%{_sbindir}/svlogd
%{_sbindir}/utmpset
%{_sbindir}/runsvdir-start
%{_mandir}/man8/*.8*
%doc doc/* etc/
%doc package/CHANGES package/COPYING package/README package/THANKS package/TODO
%dir /etc/service

%changelog