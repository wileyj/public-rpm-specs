%global with_alinux 1
%define filelist mccabe-0.6.1-filelist_python

Name:           python-mccabe
Version:        0.6.1
Release:        1.%{?dist}
Summary:        python-mccabe
Group:          Development/Languages
License:        Expat license
URL:            https://github.com/pycqa/mccabe
Provides:       python-mccabe = %{version}-%{release}
Provides:       python-mccabe = %{version}-%{release}
Obsoletes:      python-mccabe < %{version}-%{release}
Obsoletes:      python-mccabe < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros



%description


%if 0%{?with_alinux}
%package -n python27-mccabe
Summary:        python27-mccabe
Group:          Development/Languages
License:        Expat license
URL:            https://github.com/pycqa/mccabe
Provides:       python27-mccabe = %{version}-%{release}
Provides:       python27-mccabe = %{version}-%{release}
Obsoletes:      python27-mccabe < %{version}-%{release}
Obsoletes:      python27-mccabe < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros



%description -n python27-mccabe
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/06/18/fa675aa501e11d6d6ca0ae73a101b2f3571a565e0f7d38e062eec18a91ee/mccabe-0.6.1.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/mccabe-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-mccabe-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-mccabe-%{version}-%{release}
[ "%{_builddir}/python2-mccabe-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-mccabe-%{version}-%{release}
[ "%{_builddir}/python3-mccabe-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-mccabe-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-mccabe -f %{filelist}
%endif

## end file