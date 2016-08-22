Name:           apache-forrest
%define         realname apache-forrest
Summary:        software project management tool
Version:        0.9
Release:        1.%{dist}
Url:            http://forrest.apache.org
License:        Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        apache-forrest-%{version}-sources.tar.gz
Source1:        apache-forrest-%{version}-dependencies.tar.gz
#Source2:        forrest_path.sh

%description
Apache forrest

%prep
tar -xzvf %{SOURCE1}
%setup
%build

%install
rm -rf %{buildroot}
#mkdir -p %{buildroot}/etc/profile.d
#cp -R %{SOURCE2} %{buildroot}/etc/profile.d/forrest_path.sh
mkdir -p  %{buildroot}/opt/apache-forrest
cp -R * %{buildroot}/opt/apache-forrest

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
/opt/apache-forrest
#/etc/profile.d/forrest_path.sh
