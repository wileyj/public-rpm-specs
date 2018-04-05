%define filelist python-consul-0.7.2-filelist_python3

Name:           python3-python-consul
Version:        0.7.2
Release:        1.%{?dist}
Summary:        python-python-consul
Group:          Development/Languages
License:        MIT
URL:            https://github.com/cablehead/python-consul
Provides:       python3-python-consul = %{version}-%{release}
Provides:       python3-python-consul = %{version}-%{release}
Obsoletes:      python3-python-consul < %{version}-%{release}
Obsoletes:      python3-python-consul < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros

Requires: python3-twisted
Requires: python3-treq
Requires: python3-tornado
Requires: python3-aiohttp
Requires: python3-six
Requires: python3-requests


%description


%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/7a/8f/9f8eaab8826a59e1beb0808ed77bbb4b8153679ef24c0ef27011f87e4d8b/python-consul-0.7.2.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
tar -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
mv %{_builddir}/python-consul-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}

rm -rf %{py3dir}
cp -a . %{py3dir}


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py3dir}
%{__python3} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
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
' > $RPM_BUILD_DIR//%{filelist}
%{__sed} -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR//%{filelist}
exit 0


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-python-consul-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-python-consul-%{version}-%{release}
[ "%{_builddir}/python2-python-consul-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-python-consul-%{version}-%{release}
[ "%{_builddir}/python3-python-consul-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-python-consul-%{version}-%{release}



%files -f %{filelist}

## end file