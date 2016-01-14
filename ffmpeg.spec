%define ffmpeg_major    1
%define ffmpeg_minor    0
%define ffmpeg_version  %{ffmpeg_major}.%{ffmpeg_minor}
%define ffmpeg_release  1

%define _without_debug        1
%define _without_dc1394       1
%define _without_schroedinger 1
%define _without_a52dec       1
%define _without_libcaca      1
%define _without_mmx          1
%define _without_mmxext       1
%define _without_vaapi        1
%define _without_sse          1
%define _without_sse2         1
%define _without_sse3         1
%define _without_ssse3        1
%define _without_sse4         1
%define _without_armv5te      1
%define _without_armv6        1
%define _without_armv6t2      1
%define _without_armvfp       1
%define _without_amd3dnow     1
%define _without_amd3dnowext  1
%define _without_speex        1
%define _without_gnutls       1


Summary:              Utilities and libraries to record, convert and stream audio and video
Name:                 ffmpeg
Version:              %{ffmpeg_version}
Release:              %{ffmpeg_release}.%{dist}
License:              GPL
Vendor: %{vendor}
Packager: %{packager}
Group:                Applications/Multimedia
URL:                  http://ffmpeg.org/
Source:               http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.bz2
BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:        SDL-devel
BuildRequires:        freetype-devel
BuildRequires:        imlib2-devel
BuildRequires:        zlib-devel
BuildRequires:        yasm-devel
BuildRequires:        fontconfig-devel

%{!?_without_a52dec:BuildRequires: a52dec-devel}
%{!?_without_dc1394:BuildRequires: libdc1394-devel}
%{!?_without_faac:BuildRequires: faac-devel}
%{!?_without_gsm:BuildRequires: gsm-devel}
%{!?_without_lame:BuildRequires: lame-devel => 3.99.5 }
%{!?_without_nut:BuildRequires: libnut-devel => 0.0.677}
%{!?_without_opencore_amr:BuildRequires: opencore-amr-devel => 0.1.2}
%{!?_without_openjpeg:BuildRequires: libopenjpeg-devel => 1.5.1}
%{!?_without_rtmp:BuildRequires: rtmpdump-devel => 2.4, rtmpdump-librtmp0 => 2.4 }
%{!?_without_schroedinger:BuildRequires: schroedinger-devel}
%{!?_without_texi2html:BuildRequires: texi2html}
%{!?_without_theora:BuildRequires: libogg-devel => 1.3.0, libtheora-devel => 1.1.1 }
%{!?_without_vorbis:BuildRequires: libogg-devel => 1.3.0, libvorbis-devel => 1.3.2 } 
%{!?_without_vpx:BuildRequires: libvpx-devel => 1.1.0 }
%{!?_without_x264:BuildRequires: libx264-devel => 0.0.0-0.4.20121102 }
%{!?_without_xvid:BuildRequires: libxvid-devel => 1.3.2 }
%{!?_without_speex:BuildRequires: speex-devel}
%{!?_without_openssl:BuildRequires: openssl-devel => 0.9.8}
%{!?_without_gnutls:BuildRequires: gnutls-devel => 3.0.25}
%{!?_without_x11grab:BuildRequires: libXfixes-devel => 4.0.1}

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Available rpmbuild rebuild options :

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: imlib2-devel, SDL-devel, freetype-devel, zlib-devel, pkgconfig, yasm-devel, fontconfig-devel
%{!?_without_a52dec:Requires: a52dec-devel}
%{!?_without_dc1394:Requires: libdc1394-devel}
%{!?_without_faac:Requires: faac-devel}
%{!?_without_gsm:Requires: gsm-devel}
%{!?_without_lame:Requires: lame-devel => 3.99.5  }
%{!?_without_nut:BuildRequires: libnut-devel => 0.0.677}
%{!?_without_opencore_amr:BuildRequires: opencore-amr-devel => 0.1.2}
%{!?_without_openjpeg:BuildRequires: libopenjpeg-devel => 1.5.1}
%{!?_without_rtmp:BuildRequires: rtmpdump-devel => 2.4, rtmpdump-librtmp0 => 2.4 }
%{!?_without_schroedinger:BuildRequires: schroedinger-devel}
%{!?_without_texi2html:BuildRequires: texi2html}
%{!?_without_theora:BuildRequires: libogg-devel => 1.3.0, libtheora-devel => 1.1.1 }
%{!?_without_vorbis:BuildRequires: libogg-devel => 1.3.0, libvorbis-devel => 1.3.2 }
%{!?_without_vpx:BuildRequires: libvpx-devel => 1.1.0 }
%{!?_without_x264:BuildRequires: libx264-devel => 0.0.0-0.4.20121102 }
%{!?_without_xvid:BuildRequires: libxvid-devel => 1.3.2 }
%{!?_without_speex:BuildRequires: speex-devel}
%{!?_without_openssl:BuildRequires: openssl-devel => 0.9.8}
%{!?_without_gnutls:BuildRequires: gnutls-devel => 3.0.25 }

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%package libpostproc
Summary: Video postprocessing library from ffmpeg
Group: System Environment/Libraries
Provides: ffmpeg-libpostproc-devel = %{version}-%{release}
Provides: libpostproc = 1.0-1
Provides: libpostproc-devel = 1.0-1
Obsoletes: libpostproc < 1.0-1
Obsoletes: libpostproc-devel < 1.0-1
Requires: pkgconfig

%description libpostproc
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.

This package contains only ffmpeg's libpostproc post-processing library which
other projects such as transcode may use. Install this package if you intend
to use MPlayer, transcode or other similar programs.

%prep
%setup

%build
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export PATH="$PATH:%{_libdir}";

./configure \
  --prefix="%{_prefix}" \
  --libdir="%{_libdir}" \
  --shlibdir="%{_libdir}" \
  --mandir="%{_mandir}" \
  --incdir="%{_includedir}" \
  --disable-avisynth \
  --enable-gpl \
  --enable-version3 \
  --enable-nonfree \
  --enable-postproc \
  --enable-pthreads \
  --enable-shared \
  --enable-swscale \
  --enable-vdpau \
  --enable-pthreads \
  --enable-postproc \
  --enable-runtime-cpudetect \
  --enable-hwaccel=mpeg4_vaapi \
  --enable-network \
  %{!?_without_x11grab:      --enable-x11grab} \
  %{!?_without_gnutls:       --enable-gnutls} \
  %{!?_without_dc1394:       --enable-libdc1394} \
  %{!?_without_faac:         --enable-libfaac} \
  %{!?_without_gsm:          --enable-libgsm} \
  %{!?_without_lame:         --enable-libmp3lame} \
  %{!?_without_nut:          --enable-libnut} \
  %{!?_without_opencore_amr: --enable-libopencore-amrnb --enable-libopencore-amrwb} \
  %{!?_without_rtmp:         --enable-librtmp} \
  %{!?_without_schroedinger: --enable-libschroedinger} \
  %{!?_without_speex:        --enable-libspeex} \
  %{!?_without_theora:       --enable-libtheora} \
  %{!?_without_vorbis:       --enable-libvorbis} \
  %{!?_without_vpx:          --enable-libvpx} \
  %{!?_without_x264:         --enable-libx264 --enable-hwaccel=h264_vaapi --enable-hwaccel=h264_dxva2} \
  %{!?_without_xvid:         --enable-libxvid} \
  %{!?_without_openjpeg:     --enable-libopenjpeg} \
  %{?_without_v4l:           --disable-indev="v4l" --disable-indev="v4l2"} \
  %{!?_without_fontconfig:   --enable-fontconfig } \
  %{!?_without_libfreetype:  --enable-libfreetype } \
  %{!?_without_openssl:      --enable-openssl } \
  %{!?_without_librtmp:      --enable-librtmp } \
  %{!?_without_zlib:         --enable-zlib } \
  %{!?_without_sram:         --enable-sram } \
  %{!?_without_thumb:        --enable-thumb } \
  %{!?_without_pic:          --enable-pic} \
  %{?_without_random:        --disable-random} \
  %{!?_without_mmx:          --disable-mmx } \
  %{!?_without_mmxext:       --disable-mmxext } \
  %{!?_without_sse:          --disable-sse } \
  %{!?_without_sse2:         --disable-sse2 } \
  %{!?_without_sse3:         --disable-sse3 } \
  %{!?_without_ssse3:        --disable-ssse3 } \
  %{!?_without_sse4:         --disable-sse4 } \
  %{!?_without_armv5te:      --disable-armv5te } \
  %{!?_without_armv6:        --disable-armv6 } \
  %{!?_without_armv6t2:      --disable-armv6t2 } \
  %{!?_without_armvfp:       --disable-armvfp } \
  %{!?_without_amd3dnow:     --disable-amd3dnow } \
  %{!?_without_amd3dnowext:  --disable-amd3dnowext } \
  %{?_withoutout_vaapi:      --enable-vaapi } \
  %{!?_without_libcaca:      --enable-libcaca } \
  --arch=%{_target_cpu} \
  --disable-htmlpages \
  --disable-podpages \
  --disable-txtpages

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot} _docs
%{__make} install DESTDIR="%{buildroot}"

# Remove unwanted files from the included docs
%{__cp} -a doc _docs
%{__rm} -rf _docs/{Makefile,*.texi,*.pl}

# The <postproc/postprocess.h> is now at <ffmpeg/postprocess.h>, so provide
# a compatibility symlink
%{__mkdir_p} %{buildroot}%{_includedir}/postproc/
%{__ln_s} ../ffmpeg/postprocess.h %{buildroot}%{_includedir}/postproc/postprocess.h

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{_libdir}/libav{codec,device,format,util}.so.*.*.* &>/dev/null || :

%postun -p /sbin/ldconfig

%post libpostproc -p /sbin/ldconfig
%postun libpostproc -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc Changelog COPYING* CREDITS INSTALL MAINTAINERS README
%doc %{_mandir}/man1/ffprobe.1*
%doc %{_mandir}/man1/ffmpeg.1*
%doc %{_mandir}/man1/ffplay.1*
%doc %{_mandir}/man1/ffserver.1*
%{_bindir}/ffprobe
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffserver
%{_datadir}/ffmpeg/
%{_libdir}/libavcodec.so.*
%{_libdir}/libavdevice.so.*
%{_libdir}/libavfilter.so.*
%{_libdir}/libavformat.so.*
%{_libdir}/libavutil.so.*
%{_libdir}/libswscale.so.*
#%{_libdir}/vhook/

%files devel
%defattr(-, root, root, 0755)
%doc _docs/*
%{_includedir}/libavcodec/
%{_includedir}/libavdevice/
%{_includedir}/libavfilter/
%{_includedir}/libavformat/
%{_includedir}/libavutil/
%{_includedir}/libswscale/
%{_includedir}/libswresample/
%{_libdir}/libavcodec.a
%{_libdir}/libavdevice.a
%{_libdir}/libavfilter.a
%{_libdir}/libavformat.a
%{_libdir}/libavutil.a
%{_libdir}/libswscale.a
%{_libdir}/libavcodec.so
%{_libdir}/libavdevice.so
%{_libdir}/libavfilter.so
%{_libdir}/libavformat.so
%{_libdir}/libavutil.so
%{_libdir}/libswscale.so
%{_libdir}/libswresample.a
%{_libdir}/libswresample.so
%{_libdir}/libswresample.so.*
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/pkgconfig/libswscale.pc
%{_libdir}/pkgconfig/libswresample.pc

%files libpostproc
%defattr(-, root, root, 0755)
%{_includedir}/libpostproc/
%{_includedir}/postproc/
%{_libdir}/libpostproc.a
%{_libdir}/libpostproc.so*
%{_libdir}/pkgconfig/libpostproc.pc

   /usr/include/libswresample/swresample.h

%changelog

