%global with_alinux 1
%define filelist urllib3-1.22-filelist_python

Name:           python-urllib3
Version:        1.22
Release:        1.%{?dist}
Summary:        python-urllib3
Group:          Development/Languages
License:        MIT
URL:            https://urllib3.readthedocs.io/
Provides:       python-urllib3 = %{version}-%{release}
Provides:       python-urllib3 = %{version}-%{release}
Obsoletes:      python-urllib3 < %{version}-%{release}
Obsoletes:      python-urllib3 < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-PySocks
Requires: python-ipaddress
Requires: python-certifi
Requires: python-idna
Requires: python-cryptography
Requires: python-pyOpenSSL


%description


%if 0%{?with_alinux}
%package -n python27-urllib3
Summary:        python27-urllib3
Group:          Development/Languages
License:        MIT
URL:            https://urllib3.readthedocs.io/
Provides:       python27-urllib3 = %{version}-%{release}
Provides:       python27-urllib3 = %{version}-%{release}
Obsoletes:      python27-urllib3 < %{version}-%{release}
Obsoletes:      python27-urllib3 < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-PySocks
Requires: python27-ipaddress
Requires: python27-certifi
Requires: python27-idna
Requires: python27-cryptography
Requires: python27-pyOpenSSL


%description -n python27-urllib3
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/ee/11/7c59620aceedcc1ef65e156cc5ce5a24ef87be4107c2b74458464e437a5d/urllib3-1.22.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/urllib3-%{version} %{_builddir}/%{name}-%{version}
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
%__rm -rf %{buildroot}%{python_sitelib}/urllib3/packages/ssl_match_hostname/*
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
[ "%{_builddir}/python-urllib3-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-urllib3-%{version}-%{release}
[ "%{_builddir}/python2-urllib3-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-urllib3-%{version}-%{release}
[ "%{_builddir}/python3-urllib3-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-urllib3-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-urllib3 -f %{filelist}
%endif

## end file
