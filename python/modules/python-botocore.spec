%global with_alinux 0
%define filelist botocore-1.8.11-filelist_python

Name:           python-botocore
Version:        1.8.11
Release:        1.%{?dist}
Summary:        python-botocore3
Group:          Development/Languages
License:        Apache License 2.0
URL:            https://github.com/boto/botocore
Provides:       python-botocore3 = %{version}-%{release}
Provides:       python-botocore3 = %{version}-%{release}
Obsoletes:      python-botocore3 < %{version}-%{release}
Obsoletes:      python-botocore3 < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros



%description
%{summary}

%if 0%{?with_alinux}
%package -n python27-botocore
Summary:        python27-botocore
Group:          Development/Languages
License:        Apache License 2.0
URL:            https://github.com/boto/botocore
Provides:       python27-botocore = %{version}-%{release}
Provides:       python27-botocore = %{version}-%{release}
Obsoletes:      python27-botocore < %{version}-%{release}
Obsoletes:      python27-botocore < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros



%description -n python27-botocore
** Amazon Linux Python
%{summary}

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/ab/d5/d1b9290207e96fa4249830dbac3b545f5db0e9257480f5a0aa719c9e8ac6/botocore-1.8.11.tar.gz#md5=4fa791a6fe9934a7a29ebdd9300c6d84 -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/botocore-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-botocore3-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-botocore3-%{version}-%{release}
[ "%{_builddir}/python2-botocore-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-botocore3-%{version}-%{release}
[ "%{_builddir}/python3-botocore-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-botocore3-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-botocore -f %{filelist}
%endif

## end file
