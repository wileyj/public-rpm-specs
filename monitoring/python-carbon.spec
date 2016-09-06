%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%global pkgname carbon
%define pip_version 0.9.15
%define filelist %{pkgname}-%{version}-filelist

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

Name:           %{python}-%{pkgname}
Version:        %{pip_version}
Release:        1.%{dist}
Summary:        Metrics collection for graphite
Group:          Applications/Internet
License:        Apache Software License 2.0
Vendor:		%{vendor}
Packager:	%{packager}
URL:            https://launchpad.net/graphite
Source1:        %{pkgname}-cache.init
Source2:        %{pkgname}-cache.sysconfig
Source3:        %{pkgname}-relay.init
Source4:        %{pkgname}-relay.sysconfig
Source5:        %{pkgname}-aggregator.init
Source6:        %{pkgname}-aggregator.sysconfig
BuildRoot:      %{_tmppath}/%{pkgname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       %{python}-whisper, %{python}-twisted-core >= 8.0

%description
Carbon is one of the components of Graphite, and is responsible for receiving metrics over the network and writing them down to disk using a storage backend.

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://pypi.python.org/pypi/%{pkgname}/%{pip_version} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#" | tail -1`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
mv %{_builddir}/%{pkgname}-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build
#%{__python} setup.py build
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create log and var directories
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{pkgname}-cache
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{pkgname}-relay
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{pkgname}-aggregator
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{pkgname}

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{pkgname}-cache
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{pkgname}-cache
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/%{pkgname}-relay
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{pkgname}-relay
%{__install} -Dp -m0755 %{SOURCE5} %{buildroot}%{_initrddir}/%{pkgname}-aggregator
%{__install} -Dp -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{pkgname}-aggregator

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{pkgname}
%{__install} -Dp -m0644 conf/carbon.conf.example %{buildroot}%{_sysconfdir}/%{pkgname}/carbon.conf
%{__install} -Dp -m0644 conf/storage-schemas.conf.example %{buildroot}%{_sysconfdir}/%{pkgname}/storage-schemas.conf

# Create transient files in buildroot for ghosting
%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{pkgname}-cache
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{pkgname}-relay
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{pkgname}-aggregator

%{__mkdir_p} %{buildroot}%{_localstatedir}/run
%{__touch} %{buildroot}%{_localstatedir}/run/%{pkgname}-cache.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{pkgname}-relay.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{pkgname}-aggregator.pid

# no empty directories
find %{buildroot} \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    #print "%doc  src Changes examples README";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%pre
%{__getent} group %{pkgname} >/dev/null || %{__groupadd} -r %{pkgname}
%{__getent} passwd %{pkgname} >/dev/null || \
    %{__useradd} -r -g %{pkgname} -d %{_localstatedir}/lib/%{pkgname} \
    -s /sbin/nologin -c "Carbon cache daemon" %{pkgname}
exit 0

%preun
%{__service} %{pkgname} stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd %{pkgname} >/dev/null && \
      %{__userdel} -r %{pkgname} 2>/dev/null
fi
exit 0



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{name}-%{version}/%filelist
%defattr(-,root,root)

%changelog
