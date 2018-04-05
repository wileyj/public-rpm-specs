%global with_alinux 1
%define filelist redis-2.10.6-filelist_python

Name:           python-redis
Version:        2.10.6
Release:        1.%{?dist}
Summary:        python-redis
Group:          Development/Languages
License:        MIT
URL:            http://github.com/andymccurdy/redis-py
Provides:       python-redis = %{version}-%{release}
Provides:       python-redis = %{version}-%{release}
Obsoletes:      python-redis < %{version}-%{release}
Obsoletes:      python-redis < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros



%description


%if 0%{?with_alinux}
%package -n python27-redis
Summary:        python27-redis
Group:          Development/Languages
License:        MIT
URL:            http://github.com/andymccurdy/redis-py
Provides:       python27-redis = %{version}-%{release}
Provides:       python27-redis = %{version}-%{release}
Obsoletes:      python27-redis < %{version}-%{release}
Obsoletes:      python27-redis < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros



%description -n python27-redis
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/09/8d/6d34b75326bf96d4139a2ddd8e74b80840f800a0a79f9294399e212cb9a7/redis-2.10.6.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/redis-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-redis-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-redis-%{version}-%{release}
[ "%{_builddir}/python2-redis-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-redis-%{version}-%{release}
[ "%{_builddir}/python3-redis-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-redis-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-redis -f %{filelist}
%endif

## end file