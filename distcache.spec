Summary:	Distributed SSL session cache
Summary(pl):	Rozproszona pamiêæ podrêczna sesji SSL
Name:		distcache
Version:	1.4.5
Release:	0.5
License:	LGPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/distcache/%{name}-%{version}.tar.bz2
# Source0-md5:	bad485801024f711ad72e83ba1adcd7d
Source1:	dc_server.init
Source2:	dc_client.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-setuid.patch
URL:		http://www.distcache.org/
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.7
BuildRequires:	libtool
BuildRequires:	openssl-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The distcache package provides a variety of functionality for enabling
a network-based session caching system, primarily for (though not
restricted to) SSL/TLS session caching.

%description -l pl
Pakiet distcache udostêpnia rozmait± funkcjonalno¶æ maj±c± umo¿liwiæ
dzia³anie sieciowego systemu pamiêci podrêcznej sesji, g³ównie (choæ
niekoniecznie tylko) w celu zapamiêtywania sesji SSL/TLS.

%package libs
Summary:	Shared distcache distributed session cache libraries
Group:		Libraries

%description libs
This package includes the shared libraries that implement the
necessary network functionality, the session caching protocol, and
APIs for applications wishing to use a distributed session cache, or
indeed even to implement a storage mechanism for a session cache
server.

%package devel
Summary:	Header files for distcache distributed session cache library
Summary(pl):	Pliki nag³ówkowe biblioteki rozproszonej pamiêci podrêcznej sesji distcache
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package includes the header files for the libraries that
implement the necessary network functionality, the session caching
protocol, and APIs for applications wishing to use a distributed
session cache, or indeed even to implement a storage mechanism for a
session cache server.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe bibliotek implementuj±cych
potrzebn± funkcjonalno¶æ sieciow±, protokó³ zapamiêtywania sesji oraz
API dla aplikacji chc±cych korzystaæ z rozproszonej pamiêci podrêcznej
sesji lub maj±cych samemu implementowaæ mechanizm przechowywania
danych dla serwera pamiêci podrêcznej sesji.

%package static
Summary:	Static distcache distributed session cache library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package includes the static libraries that implement the
necessary network functionality, the session caching protocol, and
APIs for applications wishing to use a distributed session cache, or
indeed even to implement a storage mechanism for a session cache
server.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C ssl install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dc_server
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dc_client
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/distcache

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{nal_test,piper}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add dc_server
/sbin/chkconfig --add dc_client
%service dc_server restart "Distcache SSL Session Cache Server"
%service dc_client restart "Distcache SSL Session Cache Client Proxy"

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del dc_server
	/sbin/chkconfig --del dc_client
	%service -q dc_server stop
	%service -q dc_client stop
fi

%files
%defattr(644,root,root,755)
%doc ANNOUNCE CHANGES README LICENSE FAQ
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_bindir}/sslswamp
%attr(755,root,root) %{_bindir}/dc_*
%attr(754,root,root) /etc/rc.d/init.d/dc_*
%{_datadir}/swamp
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/distcache
%{_includedir}/libnal
%{_mandir}/man2/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
