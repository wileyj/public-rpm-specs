# http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz
# curl -L -b "oraclelicense=a" http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz -O
# curl -L -b "oraclelicense=a" http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz -O

%define __os_install_post %{nil}
%define _unpackaged_files_terminate_build 0
%define _find_requires 0
%define home /usr/java/%{name}%{version}
%define current /usr/java/current

Name:           jdk
Summary:        Sun JDK
Version:        1.8.0_66
Release:	1.%{dist}
Url:            http://java.sun.com
License:        Binary Code License Agreement
Vendor: %{vendor}
Packager: %{packager}
Group:          Development/Libraries/Java
#Buildroot:	java-build
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Source0:	%{name}-8u66-linux-x64.tar.gz
AutoReq:	0
AutoProv:	0
Provides:	jdk = %{version}
Provides:	java-openjdk = %{version}
Provides:	jre = %{version}
Provides:	java = %{version}

%description
Java Development Kit version %{version}
%prep
%setup -n %{name}%{version} -T -b 0

%build
export DONT_STRIP=1
echo "#####################"
echo %{_target_cpu}
echo "########"
echo %{_arch}
%install
export DONT_STRIP=1
rm -rf %{buildroot}
%__mkdir_p %{buildroot}%{home}
%__mkdir_p %{buildroot}%{_bindir} 
%__mkdir_p %{buildroot}/etc/profile.d
%__mkdir_p %{buildroot}/etc/ld.so.conf.d
cp -R * %{buildroot}%{home}

cat <<EOF> %{buildroot}/etc/profile.d/jdk.sh
export JAVA_HOME=%{current}
export PATH=\$PATH:%{current}/bin
export CLASSPATH=%{current}/lib
EOF

cat <<EOF> %{buildroot}/etc/ld.so.conf.d/jdk.conf
%{home}/jre/lib/amd64
EOF

#A=`pwd`
#cd %{buildroot}/usr/java
#ln -s %{home} current

ln -sf %{home}  $RPM_BUILD_ROOT%{current}
ln -sf %{current}/bin/java  $RPM_BUILD_ROOT%{_bindir}/java
ln -sf %{current}/bin/javac  $RPM_BUILD_ROOT%{_bindir}/javac
ln -sf %{current}/bin/javah  $RPM_BUILD_ROOT%{_bindir}/javah
ln -sf %{current}/bin/jar  $RPM_BUILD_ROOT%{_bindir}/jar
ln -sf %{current}/bin/javap  $RPM_BUILD_ROOT%{_bindir}/javap
ln -sf %{current}/bin/jstack  $RPM_BUILD_ROOT%{_bindir}/jstack
ln -sf %{current}/bin/jstat  $RPM_BUILD_ROOT%{_bindir}/jstat
ln -sf %{current}/bin/jstatd  $RPM_BUILD_ROOT%{_bindir}/jstatd
ln -sf %{current}/bin/jdb  $RPM_BUILD_ROOT%{_bindir}/jdb
ln -sf %{current}/bin/jmap  $RPM_BUILD_ROOT%{_bindir}/jmap

%post
ldconfig 

%postun
rm -f %{home}
ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%{home}
%{current}
%attr(755, root, root) /etc/profile.d/jdk.sh
#%{_sysconfdir}/ld.so.conf.d/jdk.conf
%{_bindir}/java
%{_bindir}/javac
%{_bindir}/javah
%{_bindir}/jar
%{_bindir}/javap
%{_bindir}/jstack
%{_bindir}/jstat
%{_bindir}/jstatd
%{_bindir}/jdb
%{_bindir}/jmap


