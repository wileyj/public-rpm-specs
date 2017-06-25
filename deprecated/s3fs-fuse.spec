%define repo https://github.com/s3fs-fuse/s3fs-fuse
%define gitversion %(echo `curl -s %{repo}/releases | grep 'span class="css-truncate-target"' | head -1 |  tr -d 'vru\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Summary: s3fs mount s3 bucket in userspace
Name: s3fs-fuse
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
License: BSD
Packager: %{packager}
Vendor: %{vendor}
Group: Applications
URL: https://github.com/s3fs-fuse/s3fs-fuse/blob/master/README
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make, fuse, fuse-devel, fuse-libs, libxml2-devel, kernel-devel, curl-devel, openssl-devel, git
Requires: fuse, fuse-libs
Provides: s3fs-fuse

%description
S3FS is FUSE (File System in User Space) based solution to mount/unmount an Amazon S3 storage buckets and use system commands with S3 just like it was another Hard Disk.

 

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
./autogen.sh
./configure
 
%build
cd %{name}-%{version}
%{__make}

%install
cd %{name}-%{version}
%{__make} install DESTDIR="%{buildroot}"

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
/usr/local/bin/s3fs
/usr/local/share/man/man1/s3fs.1
