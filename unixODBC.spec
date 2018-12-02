Summary:	unixODBC - a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl.UTF-8):	unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuksa
Name:		unixODBC
Version:	2.3.7
Release:	1
License:	LGPL v2+ (libraries), GPL v2+ (programs, News Server driver)
Group:		Libraries
Source0:	ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
# Source0-md5:	274a711b0c77394e052db6493840c6f9
URL:		http://www.unixodbc.org/
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
Obsoletes:	libunixODBC2
Obsoletes:	unixODBC-gnome
Obsoletes:	unixODBC-gnome-devel
Obsoletes:	unixODBC-gnome-static
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
Obsoletes:	libunixODBC2-devel

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

%build
%configure \
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
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{esoob,mimer,odbc{drvcfg{1,2},mini,my,nn,psql,txt},oplodbc,oraodbc,sapdb,tds}S.{la,a}
# Drivers are lt_dlopened by given name (.so or SONAME)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{nn,odbcpsql,template}.{la,a}

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
%attr(755,root,root) %{_libdir}/libodbc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbc.so.2
%attr(755,root,root) %{_libdir}/libodbc.so
%attr(755,root,root) %{_libdir}/libodbcinst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcinst.so.2
%attr(755,root,root) %{_libdir}/libodbcinst.so
# drivers
%attr(755,root,root) %{_libdir}/libesoobS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libesoobS.so.1
%attr(755,root,root) %{_libdir}/libmimerS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmimerS.so.1
%attr(755,root,root) %{_libdir}/libnn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnn.so.1
%attr(755,root,root) %{_libdir}/libodbccr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbccr.so.2
%attr(755,root,root) %{_libdir}/libodbcdrvcfg1S.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcdrvcfg1S.so.1
%attr(755,root,root) %{_libdir}/libodbcdrvcfg2S.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcdrvcfg2S.so.1
%attr(755,root,root) %{_libdir}/libodbcminiS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcminiS.so.1
%attr(755,root,root) %{_libdir}/libodbcmyS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcmyS.so.1
%attr(755,root,root) %{_libdir}/libodbcnnS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcnnS.so.1
%attr(755,root,root) %{_libdir}/libodbcpsql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcpsql.so.2
%attr(755,root,root) %{_libdir}/libodbcpsqlS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcpsqlS.so.1
#%attr(755,root,root) %{_libdir}/libodbctxt.so.*.*.*
#%attr(755,root,root) %ghost %{_libdir}/libodbctxt.so.1
%attr(755,root,root) %{_libdir}/libodbctxtS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbctxtS.so.1
%attr(755,root,root) %{_libdir}/liboplodbcS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboplodbcS.so.1
%attr(755,root,root) %{_libdir}/liboraodbcS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboraodbcS.so.1
%attr(755,root,root) %{_libdir}/libsapdbS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsapdbS.so.1
%attr(755,root,root) %{_libdir}/libtdsS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtdsS.so.1
%attr(755,root,root) %{_libdir}/libtemplate.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtemplate.so.1
# for *dlopening
%attr(755,root,root) %{_libdir}/libesoobS.so
%attr(755,root,root) %{_libdir}/libmimerS.so
%attr(755,root,root) %{_libdir}/libnn.so
%attr(755,root,root) %{_libdir}/libodbccr.so
%attr(755,root,root) %{_libdir}/libodbcdrvcfg1S.so
%attr(755,root,root) %{_libdir}/libodbcdrvcfg2S.so
%attr(755,root,root) %{_libdir}/libodbcminiS.so
%attr(755,root,root) %{_libdir}/libodbcmyS.so
%attr(755,root,root) %{_libdir}/libodbcnnS.so
%attr(755,root,root) %{_libdir}/libodbcpsql.so
%attr(755,root,root) %{_libdir}/libodbcpsqlS.so
#%attr(755,root,root) %{_libdir}/libodbctxt.so
%attr(755,root,root) %{_libdir}/libodbctxtS.so
%attr(755,root,root) %{_libdir}/liboplodbcS.so
%attr(755,root,root) %{_libdir}/liboraodbcS.so
%attr(755,root,root) %{_libdir}/libsapdbS.so
%attr(755,root,root) %{_libdir}/libtdsS.so
%attr(755,root,root) %{_libdir}/libtemplate.so
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
%{_libdir}/libodbc.la
%{_libdir}/libodbcinst.la
%{_includedir}/autotest.h
%{_includedir}/odbcinst.h
%{_includedir}/odbcinstext.h
%{_includedir}/sql.h
%{_includedir}/sqlext.h
%{_includedir}/sqlspi.h
%{_includedir}/sqltypes.h
%{_includedir}/sqlucode.h
%{_includedir}/unixodbc_conf.h
%{_includedir}/uodbc_extras.h
%{_includedir}/uodbc_stats.h
%{_pkgconfigdir}/odbc.pc
%{_pkgconfigdir}/odbccr.pc
%{_pkgconfigdir}/odbcinst.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbc.a
%{_libdir}/libodbcinst.a
