#
%define __os_install_post %{nil}
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
#%define _use_internal_dependency_generator 0
# Added this line - I had to use the specific build path of the jdk files
#%define our_find_requires %{_builddir}/java-build/usr/java/jdk1.5.0_07/find_requires
%define _unpackaged_files_terminate_build 0
%define _find_requires 0
%define  debug_package %{nil}

Name:           java-1.6.0-openjdk
%define realname jdk
Summary:        Sun JDK
Version:        1.6.0_39
Release:	1.rtg
Url:            http://java.sun.com
License:        Binary Code License Agreement
Vendor:        Rising Tide Games
Packager:      Rising Tide Games
Group:          Development/Libraries/Java
#Buildroot:	java-build
BuildRoot: 	%{_tmppath}/%{realname}-%{version}-root-%(%{__id_u} -n)
Source0:        jdk-%{version}.x86_64.tar.gz
AutoReq:	0
AutoProv:	0
Provides:	java-1.6.0-openjdk

%description
Java Development Kit version %{version}
%prep
%setup -n %{realname}-1.6.0 -T -b 0

%build
echo ""
echo ""
echo "adsfn   /builddir/build/BUILD/jdk-%{version}/usr "
echo "buildroot %{BUILDROOT}"
echo "build: $BUILDROOT"
echo ""

export DONT_STRIP=1
echo "#####################"
echo %{_target_cpu}
echo "########"
echo %{_arch}
%install
export DONT_STRIP=1
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/java/%{realname}%{version}
#mkdir -p %{buildroot}/usr/local/java
cp -R * %{buildroot}/usr/java/%{realname}%{version}/

%post

%clean
rm -rf %{buildroot}
rm -rf /builddir/build/BUILD/jdk-%{version}

%files
%defattr(-,root,root)
/usr/java/jdk%{version}
#/usr/bin/*
#/usr/local/java

