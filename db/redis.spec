%define repo https://github.com/antirez/redis
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 2

%define pid_dir %{_localstatedir}/run/redis
%define pid_file %{pid_dir}/redis.pid
%define redis_ver %{gitversion}
%define redis_rel 1.%{dist}
%define redis_group redis
%define redis_user redis
%define redis_gid 490
%define redis_uid 490

Summary: redis is a key-value database like memcached
Name: redis
Version: %{redis_ver}
Release: %{redis_rel}
License: BSD
Packager: %{packager}
Vendor: %{vendor}
Group: Applications/Multimedia
URL: http://code.google.com/p/redis/

Source2: redis.init
Source3: redis.logrotate
Source4: redis.conf
Source5: redis.service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make
Requires(post): /sbin/chkconfig /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Requires: %{name}-tools = %{version}
Provides: redis

%description
Redis is a key-value database. It is similar to memcached but the dataset is
not volatile, and values can be strings, exactly like in memcached, but also
lists and sets with atomic operations to push/pop elements.

In order to be very fast but at the same time persistent the whole dataset is
taken in memory and from time to time and/or when a number of changes to the
dataset are performed it is written asynchronously on disk. You may lose the
last few queries that is acceptable in many applications but it is as fast
as an in memory DB (beta 6 of Redis includes initial support for master-slave
replication in order to solve this problem by redundancy).

Compression and other interesting features are a work in progress. Redis is
written in ANSI C and works in most POSIX systems like Linux, *BSD, Mac OS X,
and so on. Redis is free software released under the very liberal BSD license.

%package tools
Summary: redis binaries
Group: Application/System
#Requires: redis = %{version}
%description tools
%{summary}

%package jemalloc
Summary: redis jemalloc files
Group: Application/System
Requires: redis = %{version}
%description jemalloc
%{name}-jemalloc

%package devel
Summary: redis devel files
Group: Application/System
Requires: redis = %{version}
%description devel
%{name}-devel


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
%{__make}

%install
cd %{name}-%{version}
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%{__install} -Dp -m 0755 src/redis-server %{buildroot}%{_sbindir}/redis-server
%{__install} -Dp -m 0755 src/redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
%{__install} -Dp -m 0755 src/redis-cli %{buildroot}%{_bindir}/redis-cli
%{__install} -Dp -m 0755 src/redis-check-aof %{buildroot}%{_bindir}/redis-check-aof
#%{__install} -Dp -m 0755 src/redis-check-dump %{buildroot}%{_bindir}/redis-check-dump
%{__install} -Dp -m 0755 src/redis-sentinel %{buildroot}%{_bindir}/redis-sentinel

%{__install} -Dp -m 0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/redis
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/redis
%{__install} -Dp -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/redis.conf
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/lib/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/redis
%{__install} -p -d -m 0755 %{buildroot}%{pid_dir}

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE5} %{buildroot}%{_unitdir}

pwd=`pwd`
for i in `ls deps`; do
  if [ -d deps/$i ]
  then
    if [ $i != "linenoise" -a $i != "geohash-int" ]
    then
      cd deps/$i
      make install DESTDIR=$RPM_BUILD_ROOT
      cd $pwd
    fi
  fi
done
cd $pwd



%pre
getent group %{redis_group} >/dev/null || /usr/sbin/groupadd %{redis_group} -g %{redis_gid} 2>/dev/null
getent passwd %{redis_user} >/dev/null || /usr/sbin/useradd -u %{redis_uid} -c '%{redis_user}' -g %{redis_gid} -d %{_localstatedir}/lib/redis -s /bin/false %{redis_user} 2>/dev/null



%preun
if [ $1 = 0 ]; then
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec < $term
    /sbin/service redis stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del redis
fi
%post
chown -R redis:redis %{_localstatedir}/lib/redis

%postun
if  getent passwd %{redis_user} >/dev/null; then
    %{_bindir}/userdel %{redis_user}
    if [ -d  %{_var}/run/%{name} ]; then
        %__rm -rf  %{_var}/run/%{name}
    fi
fi
#remove group
if  getent group %{redis_group} >/dev/null; then
        %{_sbindir}/groupdel %{redis_group}
    fi
fi
/usr/sbin/userdel redis
/usr/sbin/groupdel redis
/sbin/chkconfig --del redis



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
%{_sbindir}/redis-server
#%{_bindir}/redis-check-dump
%{_sysconfdir}/init.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%{_sysconfdir}/logrotate.d/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/lib/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/log/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/run/redis
%{_unitdir}/%{name}.service

%files tools
%{_bindir}/redis-benchmark
%{_bindir}/redis-cli
%{_bindir}/redis-check-aof 
%{_bindir}/redis-sentinel

%files jemalloc
/usr/local/bin/jemalloc.sh
#/usr/local/bin/pprof
/usr/local/include/jemalloc/jemalloc.h
/usr/local/lib/libjemalloc*
/usr/local/share/doc/jemalloc
/usr/local/share/man/man3/jemalloc*
/usr/local/bin/jemalloc-config
/usr/local/bin/jeprof
/usr/local/lib/pkgconfig/jemalloc.pc

%files devel
%dir %attr(0755,root,root)/usr/local/include/hiredis
%dir %attr(0755,root,root)/usr/local/include/hiredis/adapters
/usr/local/lib/libhiredis*
/usr/local/include/hiredis/adapters/*.h
/usr/local/include/hiredis/*.h
/usr/local/lib/pkgconfig/hiredis.pc
