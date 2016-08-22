%define repo https://github.com/s3fs-fuse/s3fs-fuse
%define gitversion %(echo `curl -s https://github.com/s3-fuse/s3-fuse/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)


Summary: s3fs mount s3 bucket in userspace
Name: s3fs-fuse
Version: 1.78
Release: 1.%{dist}
License: BSD
Packager: %{packager}
Vendor: %{vendor}
Group: Applications
URL: https://github.com/s3fs-fuse/s3fs-fuse/blob/master/README

Source0: %{name}-%{version}.tar.gz

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
