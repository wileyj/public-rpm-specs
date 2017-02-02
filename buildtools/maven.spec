%define repo https://github.com/apache/maven
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">maven-'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1
%define real_name apache-maven
%define bin_version 3.2.1
%define bin_prefix /opt/%{real_name}-%{bin_version}
%define maven_prefix /opt/%{name}-%{gitversion}
%define maven_symlink /opt/%{name}

Name:           maven
Summary:        source software project management tool
Version:        %{gitversion}.%{revision}
Release:        %{rel_version}.%{dist}
Url:            http://maven.apache.org
License:        Apache
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Application/Web
# require the binary apache-maven package, since mvn is required to build maven. of course it is. 
BuildRequires:	apache-maven
#Obsoletes:	apache-maven

%description
Maven is a software project management and comprehension tool. Based on
the concept of a Project Object Model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
export MAVEN_HOME=%{bin_prefix}

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
%{bin_prefix}/bin/mvn -DdistributionTargetFolder="%{buildroot}%{maven_prefix}" clean install  -DskipTests

%{__mkdir_p} %{buildroot}/etc/profile.d
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/opt
cat <<EOF> %{buildroot}/etc/profile.d/maven.sh
#export MAVEN_OPTS="-Xmx512m -Xms256m -XX:MaxPermSize=256m"
export MAVEN_HOME=%{maven_prefix}
export PATH="\$PATH:%{maven_symlink}/bin"
EOF
ARCHIVE=`ls %{_builddir}/%{name}-%{version}/%{real_name}/target/%{real_name}-*-SNAPSHOT-bin.tar.gz`
DIR=`basename ${ARCHIVE} | sed -e 's/.tar.gz//g'`
EXTRACTED=`basename ${ARCHIVE} | sed -e 's/-bin.tar.gz//g'`
tar -xzvf ${ARCHIVE} -C %{buildroot}/opt
%__mv  %{buildroot}/opt/${EXTRACTED} %{buildroot}/%{maven_prefix}
%__ln_s -f %{maven_prefix} %{buildroot}%{maven_symlink}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{maven_prefix}
%{maven_prefix}/*
%{maven_symlink}
/etc/profile.d/maven.sh

