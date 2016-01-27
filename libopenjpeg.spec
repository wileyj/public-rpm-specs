%define base_version 2
%define base_rev 1
%define bname openjpeg
%global _default_patch_fuzz 2
%global repo https://github.com/uclouvain/openjpeg.git

Name:    	libopenjpeg
Version: 	%{base_version}.%{base_rev}
Release: 	2.%{dist}
Summary: 	OpenJPEG command line tools
Group:     	Applications/Multimedia
License:   	BSD
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:       	http://www.openjpeg.org/
BuildRoot: 	%{_tmppath}/%{bname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: 	libtiff-devel
Requires: 	%{name}-libs = %{version}-%{release}
#Patch50: 	openjpeg-1.3-libm.patch

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package libs
Summary: JPEG 2000 codec library
Group:   System Environment/Libraries

%description libs
The openjpeg-libs package contains runtime libraries for applications that use
OpenJPEG.

%package  devel
Summary:  Development files for openjpeg
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
The openjpeg-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%prep 
%setup -q -c -T

if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}

cmake .
#%{__make} %{?_smp_mflags}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%__mv %{buildroot}/usr/local/bin %{buildroot}%{_bindir}
%__mv %{buildroot}/usr/local/lib %{buildroot}%{_libdir}
%__mv %{buildroot}/usr/local/include %{buildroot}%{_includedir}
%__rm -rf %{buildroot}/usr/local/include
#install -m 0644  src/lib/openjp2/openjpeg.h %{buildroot}/usr/local/include/%{bname}-%{version}/openjpeg.h
install -m 0644  src/lib/openjp2/openjpeg.h %{buildroot}%{_includedir}/%{bname}-%{version}/openjpeg.h


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/opj_compress
%{_bindir}/opj_decompress
%{_bindir}/opj_dump
#%{_bindir}/extract_j2k_from_mj2
#%{_bindir}/frames_to_mj2
#%{_bindir}/image_to_j2k
#%{_bindir}/j2k_to_image
#%{_bindir}/mj2_to_frames
#%{_bindir}/wrap_j2k_in_mj2
#%{_bindir}/JPWL_image_to_j2k
#%{_bindir}/JPWL_j2k_to_image
#%{_bindir}/j2k_dump
#%{_bindir}/jpip_to_j2k
#%{_bindir}/jpip_to_jp2
#%{_bindir}/opj_dec_server
#%{_bindir}/test_index
#%{_bindir}/frames_to_mj2
#%{_bindir}/image_to_j2k
#%{_bindir}/j2k_to_image
#%{_bindir}/mj2_to_frames
#%{_bindir}/wrap_j2k_in_mj2
#%{_bindir}/JPWL_image_to_j2k
#%{_bindir}/JPWL_j2k_to_image
#%{_bindir}/j2k_dump
#%{_bindir}/jpip_to_j2k
#%{_bindir}/jpip_to_jp2
#%{_bindir}/opj_dec_server
#%{_bindir}/test_index
#%{_bindir}/extract_j2k_from_mj2
#/usr/share/doc/openjpeg-2/LICENSE
#%{_docdir}/%{bname}-%{base_version}/LICENSE

%files libs
%defattr(-,root,root,-)
%{_libdir}/libopenjp*
%{_libdir}/%{bname}-%{version}
%{_libdir}/pkgconfig/*.pc


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{bname}-%{version}/*.h
%dir %{_includedir}/%{bname}-%{version}

%changelog
