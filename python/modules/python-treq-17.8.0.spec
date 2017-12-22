%global with_alinux 1
%define filelist treq-17.8.0-filelist_python

Name:           python-treq
Version:        17.8.0
Release:        1.%{?dist}
Summary:        python-treq
Group:          Development/Languages
License:        MIT/X
URL:            https://github.com/twisted/treq
Provides:       python-treq = %{version}-%{release}
Provides:       python-treq = %{version}-%{release}
Obsoletes:      python-treq < %{version}-%{release}
Obsoletes:      python-treq < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-httpbin
Requires: python-sphinx
Requires: python-pyflakes
Requires: python-pep8
Requires: python-mock
Requires: python-attrs
Requires: python-Twisted[tls]
Requires: python-six
Requires: python-requests
Requires: python-incremental


%description


%if 0%{?with_alinux}
%package -n python27-treq
Summary:        python27-treq
Group:          Development/Languages
License:        MIT/X
URL:            https://github.com/twisted/treq
Provides:       python27-treq = %{version}-%{release}
Provides:       python27-treq = %{version}-%{release}
Obsoletes:      python27-treq < %{version}-%{release}
Obsoletes:      python27-treq < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-httpbin
Requires: python27-sphinx
Requires: python27-pyflakes
Requires: python27-pep8
Requires: python27-mock
Requires: python27-attrs
Requires: python27-Twisted[tls]
Requires: python27-six
Requires: python27-requests
Requires: python27-incremental


%description -n python27-treq
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/11/3e/1014f26bfd4d07db015ad48384446b3bdc4de4bbdd2eba3be7fbb149cc44/treq-17.8.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/treq-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-treq-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-treq-%{version}-%{release}
[ "%{_builddir}/python2-treq-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-treq-%{version}-%{release}
[ "%{_builddir}/python3-treq-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-treq-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-treq -f %{filelist}
%endif

## end file