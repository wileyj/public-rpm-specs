%define url https://github.com/s3tools/s3cmd
%define pkgname s3cmd
%define _summary        %(echo `curl -s %{url} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define repo %{url}.git
%define gitversion %(echo `curl -s %{url}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d 'v\\-</span class="css-truncate-target">'`)
%define filelist %{pkgname}-%{version}-filelist

Name:           %{pkgname}
Version:        %{gitversion}
Release:        1.%{dist}
Summary:        %{_summary}
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
URL:            %{url}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27, python27-devel, python27-setuptools
BuildRequires: git python-srpm-macros
Requires:       python27

%include /usr/lib/rpm/macros.d/macros.python
%description
%{_summary}

%setup -q -c -T

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install  --root $RPM_BUILD_ROOT


(
    echo '%defattr(-,root,root,-)'
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}"' >> %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{provider}.%{provider_tld}/mitchellh/iochan"' >> %{name}-%{version}-filelist
echo '"%{gopath}/src/%{provider}.%{provider_tld}/mitchellh/iochan*"' >> %{name}-%{version}-filelist
%{__sed} -i -e 's/%dir ""//g' %{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{name}-%{version}-filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{name}-%{version}/%filelist
%defattr(-,root,root)
%{_mandir}/man1/%{name}.1.gz
%changelog
