%global with_alinux 1
%define filelist docker-2.6.1-filelist_python

Name:           python-docker
Version:        2.6.1
Release:        1.%{?dist}
Summary:        python-docker
Group:          Development/Languages
License:        Apache License 2.0
URL:            https://github.com/docker/docker-py
Provides:       python-docker = %{version}-%{release}
Provides:       python-docker = %{version}-%{release}
Obsoletes:      python-docker < %{version}-%{release}
Obsoletes:      python-docker < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros



%description


%if 0%{?with_alinux}
%package -n python27-docker
Summary:        python27-docker
Group:          Development/Languages
License:        Apache License 2.0
URL:            https://github.com/docker/docker-py
Provides:       python27-docker = %{version}-%{release}
Provides:       python27-docker = %{version}-%{release}
Obsoletes:      python27-docker < %{version}-%{release}
Obsoletes:      python27-docker < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros



%description -n python27-docker
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/20/73/3bb05004dcc734182d57a1c8a802732e05788678a71bfa12348a614d5d73/docker-2.6.1.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/docker-%{version} %{_builddir}/%{name}-%{version}
%{__chmod} -R u+w %{_builddir}/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}

%__rm -rf %{py2dir}
%__cp -a . %{py2dir}


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python27} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python27} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%{__perl} -MFile::Find -le '
    find ({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
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
' > $RPM_BUILD_DIR//%{filelist}
%__sed -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR/%{filelist}
exit 0


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-docker-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-docker-%{version}-%{release}
[ "%{_builddir}/python2-docker-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-docker-%{version}-%{release}
[ "%{_builddir}/python3-docker-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-docker-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-docker -f %{filelist}
%endif

## end file