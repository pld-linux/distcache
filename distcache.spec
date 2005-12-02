
Summary:	Distributed SSL session cache
Name:		distcache
Version:	1.4.5
Release:	6
License:	LGPL
Group:		System Environment/Daemons
######		Unknown group!
URL:		http://www.distcache.org/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.4.5-setuid.patch
Source1:	dc_server.init
Source2:	dc_client.init
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	automake >= 1.7
BuildRequires:	autoconf >= 2.50
BuildRequires:	libtool
BuildRequires:	openssl-devel
Requires:	/sbin/chkconfig

%description
The distcache package provides a variety of functionality for enabling
a network-based session caching system, primarily for (though not
restricted to) SSL/TLS session caching.

%package devel
Group:		Development/Libraries
Summary:	Development tools for distcache distributed session cache
Requires:	distcache = %{version}

%description devel
This package includes the libraries that implement the necessary
network functionality, the session caching protocol, and APIs for
applications wishing to use a distributed session cache, or indeed
even to implement a storage mechanism for a session cache server.

%prep
%setup -q
%patch0 -p1 -b .setuid

%build
libtoolize --force --copy && aclocal && autoconf
automake -aic --gnu || : automake ate my hamster
%configure --enable-shared
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C ssl install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install $RPM_SOURCE_DIR/dc_server.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_server
install $RPM_SOURCE_DIR/dc_client.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_client

install -d $RPM_BUILD_ROOT%{_sbindir}

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{nal_test,piper}

%post
/sbin/chkconfig --add dc_server
/sbin/chkconfig --add dc_client
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
	/sbin/service dc_server stop > /dev/null 2>&1
	/sbin/service dc_client stop > /dev/null 2>&1
	/sbin/chkconfig --del dc_server
	/sbin/chkconfig --del dc_client
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sslswamp
%attr(755,root,root) %{_bindir}/dc_*
%attr(754,root,root) /etc/rc.d/init.d/dc_*
%doc ANNOUNCE CHANGES README LICENSE FAQ
%attr(755,root,root) %{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/swamp

%files devel
%defattr(644,root,root,755)
%{_includedir}/distcache
%{_includedir}/libnal
%{_libdir}/*.*a
%attr(755,root,root) %{_libdir}/*.so
%{_mandir}/man2/*
