Summary:	unixODBC - a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl.UTF-8):	unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuksa
Name:		unixODBC
Version:	2.3.14
Release:	1
License:	LGPL v2+ (libraries), GPL v2+ (programs, News Server driver)
Group:		Libraries
Source0:	ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
# Source0-md5:	316cede4896eb768fe4572d71dc04537
Patch0:		%{name}-bool.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-proto.patch
URL:		https://www.unixodbc.org/
BuildRequires:	flex
BuildRequires:	libltdl-devel >= 2:2
BuildRequires:	readline-devel >= 4.2
BuildConflicts:	kdesupport-odbc
Requires(post):	/sbin/ldconfig
%ifarch %{x8664} ia64 ppc64 sparc64 s390x
Provides:	libodbc.so()(64bit)
Provides:	libodbcinst.so()(64bit)
%else
Provides:	libodbc.so
Provides:	libodbcinst.so
%endif
Obsoletes:	libunixODBC2 < 3
Obsoletes:	unixODBC-gnome < 2.2.14
Obsoletes:	unixODBC-gnome-devel < 2.2.14
Obsoletes:	unixODBC-gnome-static < 2.2.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
unixODBC is a complete, free/open, ODBC solution for UNIX/Linux.

%description -l pl.UTF-8
unixODBC - kompletne, darmowe/otwarte ODBC dla systemów UNIX/Linux.

%package devel
Summary:	unixODBC header files and development documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokunentacja do unixODBC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libltdl-devel
Obsoletes:	libunixODBC2-devel < 3

%description devel
unixODBC header files and development documentation.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokunentacja do unixODBC.

%package static
Summary:	unixODBC static libraries
Summary(pl.UTF-8):	Biblioteki statyczne unixODBC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
unixODBC static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne unixODBC.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
CPPFLAGS="%{rpmcppflags} -D_DEFAULT_SOURCE"
%configure \
	--enable-driver-config \
	--enable-drivers \
	--enable-driverc \
	--enable-static \
	--without-included-ltdl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

:> $RPM_BUILD_ROOT%{_sysconfdir}/odbc.ini
:> $RPM_BUILD_ROOT%{_sysconfdir}/odbcinst.ini

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf doc-install
cp -a doc doc-install
find doc-install  -name 'Makefile*' | xargs -r %{__rm}

# libodbccr.so.1 is lt_dlopened
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libodbccr.{la,a}
# Setup drivers are lt_dlopened by given name (.so or SONAME)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{esoob,mimer,odbc{drvcfg{1,2},mini,my,nn,psql,txt},oplodbc,oraodbc,sapdb,tds}S.la
# Drivers are lt_dlopened by given name (.so or SONAME)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{nn,odbcpsql,template}.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libodbc{,inst}.la

# (temporarily) missing in make install
install include/autotest.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# install text driver
/usr/bin/odbcinst -i -d -r <<EOF
[TXT]
Description = Text file driver
#Driver = %{_libdir}/libodbctxt.so.1
Setup = %{_libdir}/libodbctxtS.so.1
EOF
# install postgresql driver
/usr/bin/odbcinst -i -d -r <<EOF
[PostgreSQL]
Description = PostgreSQL driver
Driver = %{_libdir}/libodbcpsql.so.2
Setup = %{_libdir}/libodbcpsqlS.so.1
EOF

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc-install/AdministratorManual doc-install/UserManual
%attr(755,root,root) %{_bindir}/dltest
%attr(755,root,root) %{_bindir}/isql
%attr(755,root,root) %{_bindir}/iusql
%attr(755,root,root) %{_bindir}/odbcinst
# can be useful not only for development
%attr(755,root,root) %{_bindir}/odbc_config
%attr(755,root,root) %{_bindir}/slencheck
# some apps dlopen these by *.so
%{_libdir}/libodbc.so.*.*.*
%ghost %{_libdir}/libodbc.so.2
%{_libdir}/libodbc.so
%{_libdir}/libodbcinst.so.*.*.*
%ghost %{_libdir}/libodbcinst.so.2
%{_libdir}/libodbcinst.so
# drivers
%{_libdir}/libnn.so.*.*.*
%ghost %{_libdir}/libnn.so.1
%{_libdir}/libodbccr.so.*.*.*
%ghost %{_libdir}/libodbccr.so.2
%{_libdir}/libodbcpsql.so.*.*.*
%ghost %{_libdir}/libodbcpsql.so.2
%{_libdir}/libtemplate.so.*.*.*
%ghost %{_libdir}/libtemplate.so.1
# drivers for dlopening
%{_libdir}/libnn.so
%{_libdir}/libodbccr.so
%{_libdir}/libodbcpsql.so
%{_libdir}/libtemplate.so
# driver config modules
%{_libdir}/libesoobS.so
%{_libdir}/libmimerS.so
%{_libdir}/libodbcdrvcfg1S.so
%{_libdir}/libodbcdrvcfg2S.so
%{_libdir}/libodbcminiS.so
%{_libdir}/libodbcmyS.so
%{_libdir}/libodbcnnS.so
%{_libdir}/libodbcpsqlS.so
%{_libdir}/libodbctxtS.so
%{_libdir}/liboplodbcS.so
%{_libdir}/liboraodbcS.so
%{_libdir}/libsapdbS.so
%{_libdir}/libtdsS.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/odbc.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/odbcinst.ini
%dir %{_sysconfdir}/ODBCDataSources
%{_mandir}/man1/dltest.1*
%{_mandir}/man1/isql.1*
%{_mandir}/man1/iusql.1*
%{_mandir}/man1/odbc_config.1*
%{_mandir}/man1/odbcinst.1*
%{_mandir}/man5/odbc.ini.5*
%{_mandir}/man5/odbcinst.ini.5*
%{_mandir}/man7/unixODBC.7*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog doc-install/{ProgrammerManual,lst}
%{_includedir}/autotest.h
%{_includedir}/odbcinst.h
%{_includedir}/odbcinstext.h
%{_includedir}/sql.h
%{_includedir}/sqlext.h
%{_includedir}/sqlspi.h
%{_includedir}/sqltypes.h
%{_includedir}/sqlucode.h
%{_includedir}/uodbc_extras.h
%{_includedir}/uodbc_stats.h
%{_includedir}/unixodbc.h
%{_includedir}/unixODBC
%{_pkgconfigdir}/odbc.pc
%{_pkgconfigdir}/odbccr.pc
%{_pkgconfigdir}/odbcinst.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbc.a
%{_libdir}/libodbcinst.a
