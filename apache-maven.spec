Name:           apache-maven
%define         realname apache-maven 
Summary:        software project management tool
Version:        3.3.9
Release:        1.%{dist}
Url:            http://maven.apache.org
License:        Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-bin.tar.gz
Source1:        maven_path.sh

%description
Maven is a software project management and comprehension tool. Based on
the concept of a Project Object Model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.
%prep
%setup
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
cp -R %{SOURCE1} %{buildroot}/etc/profile.d/maven_path.sh
mkdir -p %{buildroot}/opt/apache-maven-%{version}
cp -R . %{buildroot}/opt/apache-maven-%{version}

%post
if [ -e /opt/apache-maven ]; then
  if [ ! -h /opt/apache-maven ]; then
    echo "/opt/apache-maven is NOT a symlink, cannot create symlink"
    exit 1;
  fi
else 
  ln -s /opt/apache-maven-%{version} /opt/apache-maven
fi
if [ ! -h "/usr/local/bin/mvn" ] || [ ! -h "/usr/local/bin/mvnDebug"]; then
  ln -s /opt/apache-maven/bin/mvn /usr/local/bin/mvn
  ln -s /opt/apache-maven/bin/mvnDebug /usr/local/bin/mvnDebug
else
  echo "Cannot create maven symlinks, exiting!!"
  exit 1;
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,www)
/opt/apache-maven-%{version}
/etc/profile.d/maven_path.sh

