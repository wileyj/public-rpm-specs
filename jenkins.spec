%define _prefix	/opt/jenkins
%define workdir	/opt/jenkins/home

Name:		jenkins
Version:	1.638
Release:	1.%{dist}
Summary:	Continous Build Server
Source:		jenkins.war
Source1:	jenkins.init.in
Source2:	jenkins.sysconfig.in
Source3:	jenkins.logrotate
URL:		http://jenkins-ci.org/
Group:		Development/Tools/Building
License:	MIT/X License, GPL/CDDL, ASL2
Vendor: %{vendor}
Packager: %{packager}
BuildRoot:	%{_tmppath}/build-%{name}-%{version}
Obsoletes:  	hudson
PreReq:		/usr/sbin/lgroupadd /usr/sbin/luseradd
#PreReq:	%{fillup_prereq}
BuildArch:	noarch
Requires: 	jdk

%description
Jenkins monitors executions of repeated jobs, such as building a software
project or jobs run by cron. Among those things, current Jenkins focuses on the
following two jobs:
- Building/testing software projects continuously, just like CruiseControl or
  DamageControl. In a nutshell, Jenkins provides an easy-to-use so-called
  continuous integration system, making it easier for developers to integrate
  changes to the project, and making it easier for users to obtain a fresh
  build. The automated, continuous build increases the productivity.
- Monitoring executions of externally-run jobs, such as cron jobs and procmail
  jobs, even those that are run on a remote machine. For example, with cron,
  all you receive is regular e-mails that capture the output, and it is up to
  you to look at them diligently and notice when it broke. Jenkins keeps those
  outputs and makes it easy for you to notice when something is wrong.




Authors:
--------
    Kohsuke Kawaguchi <Kohsuke.Kawaguchi@sun.com>

%prep
%setup -q -T -c

%build

%install
rm -rf "%{buildroot}"
%__install -D -m0644 "%{SOURCE0}" "%{buildroot}%{_prefix}/%{name}.war"
%__install -d "%{buildroot}%{workdir}"
%__install -d "%{buildroot}%{workdir}/plugins"

%__install -d "%{buildroot}/var/log/jenkins"
%__install -d "%{buildroot}/var/cache/jenkins"

%__install -D -m0755 "%{SOURCE1}" "%{buildroot}/etc/init.d/%{name}"
%__sed -i 's,@@WAR@@,%{_prefix}/%{name}.war,g' "%{buildroot}/etc/init.d/%{name}"
%__install -d "%{buildroot}/usr/sbin"
%__ln_s "../../etc/init.d/%{name}" "%{buildroot}/usr/sbin/rc%{name}"

%__install -D -m0600 "%{SOURCE2}" "%{buildroot}/etc/sysconfig/%{name}"
%__sed -i 's,@@HOME@@,%{workdir},g' "%{buildroot}/etc/sysconfig/%{name}"

%__install -D -m0644 "%{SOURCE3}" "%{buildroot}/etc/logrotate.d/%{name}"

%pre
/usr/sbin/lgroupadd -r jenkins &>/dev/null || :
# SUSE version had -o here, but in Fedora -o isn't allowed without -u
/usr/sbin/luseradd -g jenkins -s /bin/false -r -c "Jenkins Continuous Build server" \
	-d "%{workdir}" jenkins &>/dev/null || :

%post
/sbin/chkconfig --add jenkins

# If we have an old hudson install, rename it to jenkins
if test -d /var/lib/hudson; then
    # leave a marker to indicate this came from Hudson.
    # could be useful down the road
    # This also ensures that the .??* wildcard matches something
    touch /var/lib/hudson/.moving-hudson
    mv -f /var/lib/hudson/* /var/lib/hudson/.??* /var/lib/jenkins
    rmdir /var/lib/hudson
    find /var/lib/jenkins -user hudson -exec chown jenkins {} + || true
fi
if test -d /var/run/hudson; then
    mv -f /var/run/hudson/* /var/run/jenkins
    rmdir /var/run/hudson
fi


%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    /sbin/service jenkins stop > /dev/null 2>&1
    /sbin/chkconfig --del jenkins
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service jenkins condrestart > /dev/null 2>&1
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/%{name}.war
%attr(0755,jenkins,jenkins) %dir %{workdir}
%attr(0750,jenkins,jenkins) /var/log/jenkins
%attr(0750,jenkins,jenkins) /var/cache/jenkins
%config /etc/logrotate.d/%{name}
%config(noreplace) /etc/init.d/%{name}
%config(noreplace) /etc/sysconfig/%{name}
/usr/sbin/rc%{name}

%changelog
