Summary:	unixODBC - a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl):	unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuxa
Name:		unixODBC
Version:	2.0.8
Release:	2
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	Библиотеки
Group(uk):	Б╕бл╕отеки
Source0:	ftp://ftp.easysoft.com/pub/beta/%{name}/%{name}-%{version}.tar.gz
Source1:	DataManager.desktop
Source2:	ODBCConfig.desktop
Source3:	odbcinst.ini
Source4:	%{name}.png
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ac_fix.patch
Icon:		unixODBC.xpm
#BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel >= 4.2
#BuildRequires:	qt-devel >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildConflicts:	kdesupport-odbc

%define		_sysconfdir	/etc

%description
unixODBC is a complete, free/open, ODBC solution for UNIX/Linux.

%description -l pl
unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuxa.

%package devel
Summary:	unixODBC header files and development documentation
Summary(pl):	Pliki nagЁСwkowe i dokunentacja do unixODBC 
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}

%description devel
unixODBC header files and development documentation.

%description -l pl
Pliki nagЁСwkowe i dokunentacja do unixODBC.

%package static
Summary:	unixODBC static libraries
Summary(pl):	Biblioteki statyczne unixODBC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}-devel = %{version}

%description static
unixODBC static libraries.

%description -l pl static
Biblioteki statyczne unixODBC.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
rm -f missing config.guess config.sub
aclocal
autoconf
automake -a -c
(cd libltdl ; autoconf)
%configure \
	--disable-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static 
# GUI requires QT2	
#	--enable-gui 
#	--with-qt-dir=%{_prefix} 
%{__make} 

# avoid relinking in some dirs
for f in cur/libodbccr.la samples/libboundparam.la ; do
	sed -e '/^relink_command/d' $f > $f.new
	mv -f $f.new $f
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/System,%{_pixmapsdir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

#install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/System
#install %{SOURCE4} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS NEWS

find doc -name Makefile\* -exec rm {} \;

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,NEWS}.gz doc/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 size mtime)  %{_sysconfdir}/odbc*.ini
#%{_applnkdir}/System/*
#%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
#doc {AUTHORS,NEWS}.gz doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%attr(644,root,root) 
%{_libdir}/lib*.a
