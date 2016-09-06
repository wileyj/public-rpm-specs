%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%global pkgname graphite-web
#%define pip_version %(echo `curl -s https://pypi.python.org/pypi/%{pkgname} | grep "<title>" | awk '{print $2}'`)
%define pip_version 0.9.15
%define filelist %{pkgname}-%{version}-filelist

%define __touch    /bin/touch
%define __service  /sbin/service

Name:           %{python}-%{pkgname}
Version:        %{pip_version}
Release:        3.%{dist}
Summary:        Enterprise scalable realtime graphing
Group:          Applications/Internet
License:        Apache License
URL:            https://launchpad.net/graphite
Vendor: %{vendor}
Packager: %{packager}
BuildRoot:      %{_tmppath}/%{pkgname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       Django django-tagging httpd mod_wsgi pycairo python-simplejson
Requires: 	bitmap-fonts-compat

%description
Graphite consists of a storage backend and a web-based visualization frontend.
Client applications send streams of numeric time-series data to the Graphite
backend (called carbon), where it gets stored in fixed-size database files
similar in design to RRD. The web frontend provides 2 distinct user interfaces
for visualizing this data in graphs as well as a simple URL-based API for
direct graph generation.

Graphite's design is focused on providing simple interfaces (both to users and
applications), real-time visualization, high-availability, and enterprise
scalability.

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://pypi.python.org/pypi/%{pkgname}/%{pip_version} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#" | tail -2 | grep 1`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
mv %{_builddir}/%{pkgname}-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create var directory with ghost files
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{pkgname}
%{__touch} %{buildroot}%{_localstatedir}/lib/%{pkgname}/graphite.db

# Create log directory with ghost files
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{pkgname}
%{__touch} %{buildroot}%{_localstatedir}/log/%{pkgname}/access.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{pkgname}/error.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{pkgname}/exception.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{pkgname}/info.log

# Create config directory and install configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{pkgname}
%{__install} -Dp -m0644 conf/dashboard.conf.example %{buildroot}%{_sysconfdir}/%{pkgname}/dashboard.conf
%{__install} -Dp -m0644 webapp/graphite/local_settings.py.example %{buildroot}%{_sysconfdir}/%{pkgname}/local_settings.py

# Install the example wsgi controller and vhost configuration
%{__install} -Dp -m0755 conf/graphite.wsgi.example %{buildroot}/usr/share/graphite/%{pkgname}.wsgi
%{__install} -Dp -m0644 examples/example-graphite-vhost.conf %{buildroot}/usr/share/graphite/%{pkgname}.apache_example

# Create local_settings symlink
%{__mkdir_p} %{buildroot}%{python_sitelib}/graphite
%{__ln_s} %{_sysconfdir}/%{pkgname}/local_settings.py %{buildroot}%{python_sitelib}/graphite/local_settings.py

# no empty directories
find %{buildroot}             \
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
echo %{_sysconfdir}/%{pkgname}/local_settings.pyc >> %filelist
echo %{_sysconfdir}/%{pkgname}/local_settings.pyo >> %filelist
%post
# Initialize the database
%{__python} %{python_sitelib}/graphite/manage.py syncdb --noinput >/dev/null
%{__chown} apache:apache %{_localstatedir}/lib/%{pkgname}/graphite.db

%posttrans
# TEMPORARY FIX
#
# The 0.9.8-x versions of this RPM symlinked local_settings.py in during %post
# and removed it during %preun. This was replaced in 0.9.9-1 with a standard
# %files entry.
#
# When upgrading from 0.9.8 to 0.9.9 the %preun action of the previous version
# removes the %files entry of the new version. This check reinstates the
# symlink. It does not affect fresh installs and can be removed in subsequent
# releases.
[ -e %{python_sitelib}/graphite/local_settings.py ] || \
    %{__ln_s} %{_sysconfdir}/%{pkgname}/local_settings.py %{python_sitelib}/graphite/local_settings.py

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{name}-%{version}/%filelist
%defattr(-,root,root)

%changelog
