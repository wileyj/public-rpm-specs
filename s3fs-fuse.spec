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
BuildRequires: gcc, make, fuse >= 2.8.4, libxml2-devel, kernel-devel, curl-devel, openssl-devel, git
Requires: fuse >= 2.8.4, fuse-libs >= 2.8.4
Provides: s3fs-fuse

%description
S3FS is FUSE (File System in User Space) based solution to mount/unmount an Amazon S3 storage buckets and use system commands with S3 just like it was another Hard Disk.


%prep
%setup -n %{name}-%{version}
git pull
./autogen.sh
./configure

%build
%{__make}
%install
%{__make} install DESTDIR="%{buildroot}"

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
/usr/local/bin/s3fs
/usr/local/share/man/man1/s3fs.1
