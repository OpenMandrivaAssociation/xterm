%define	Summary	The standard terminal emulator for the X Window System

Summary:	%{Summary}
Name:		xterm
Version:	235
Release:	%mkrel 1
Source0:	ftp://invisible-island.net/xterm/%{name}-%{version}.tgz
Source1:	ftp://invisible-island.net/xterm/%{name}-%{version}.tgz.asc
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png

# from http://www.vim.org/scripts/script.php?script_id=1349, public domain
Source20:   colortest.pl

Url:		http://invisible-island.net/xterm/
License:	MIT
Group:		Terminals
BuildRequires: libxrender-devel
BuildRequires: libxmu-devel
BuildRequires: libxext-devel
BuildRequires: libxt-devel
BuildRequires: libxau-devel
BuildRequires: libxdmcp-devel
BuildRequires: libxp-devel
BuildRequires: libxaw-devel
BuildRequires: libxpm-devel
BuildRequires: libxft-devel
BuildRequires: libncurses-devel
BuildRequires: luit
BuildRoot: %{_tmppath}/%{name}-%{version}-%{version}-buildroot
Conflicts: XFree86 < 3.3.6-13mdk
Requires: luit
Requires(post,postun):	update-alternatives

%description
The XTerm program is the standard terminal emulator for the X Window System. It
provides DEC VT102/VT220 and Tektronix 4014 compatible terminals for programs
that can't use the window system directly. If the underlying operating system
supports terminal resizing capabilities (for example, the SIGWINCH signal in
systems derived from 4.3bsd), xterm will use the facilities to notify programs
running in the window whenever it is resized.

The xterm included in this package has support for 256 colors enabled.

%prep
%setup -q
cp %{SOURCE20} .

%build
%configure \
   --disable-full-tgetent \
   --enable-wide-chars \
   --x-includes=%{_includedir}/freetype2 \
   --enable-luit \
   --enable-256-color \
   --with-app-defaults=%{_libdir}/X11/app-defaults

%make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# NOTE: encodingMode: locale means to follow the charset encoding of the
# locale. A quite complete unicode font is set as the default (instead of the
# very poor "fixed" one). a quick cat is used instead of patching the sources;
# it shoulmd be made the default imho
# locale: true means to use luit to convert locale encoding to unicode
# for display.
# luit support is needed for it to work -- pablo
cat << EOF >> $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XTerm

*.vt100.font: -misc-fixed-medium-r-normal--15-140-75-75-c-90-iso10646-1
*.vt100.encodingMode: locale
*.locale: true
*.PtyInitialErase: on
*.backarrowKeyIsErase: on
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XTerm
Comment=%Summary
Exec=%{name} -name Terminal
Icon=xterm-terminal
Terminal=false
Type=Application
StartupNotify=true
Categories=TerminalEmulator;System;Utility;
EOF

for xpm in xterm{-color_32x32,-color_48x48,_32x32,_48x48}.xpm; do
	rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/$xpm
done
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{_sourcedir}/xterm-16x16.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/xterm-terminal.png
install -m 644 %{_sourcedir}/xterm-32x32.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/xterm-terminal.png
install -m 644 %{_sourcedir}/xterm-48x48.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/xterm-terminal.png

%if 0
## strange, if xterm isn't launched with -name xxxx parameter it doesn't
## take in account the ressources --> wrong font in unicode mode --> segfault
## there is not time to fix the sources; using a script to ensure there
## is always a -nae xxxx used (pablo)
mv $RPM_BUILD_ROOT%{_bindir}/xterm $RPM_BUILD_ROOT%{_bindir}/xterm.real
cat << EOF >> $RPM_BUILD_ROOT%{_bindir}/xterm
#!/bin/bash

if echo "\$@" | grep -- '-name' >&/dev/null ; then
	 exec %{_bindir}/xterm.real "\$@"
else exec %{_bindir}/xterm.real -name Terminal "\$@"
fi
EOF
chmod a+rx $r%{_bindir}/xterm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor
update-alternatives --install %{_bindir}/xvt xvt %{_bindir}/xterm 18 || :

%postun
%clean_menus
%update_icon_cache hicolor
[[ "$1" = "0" ]] && update-alternatives --remove xvt %{_bindir}/xterm || :

%files
%defattr(-,root,root)
%doc ctlseqs.txt colortest.pl
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/X11/app-defaults/*
%_datadir/applications/mandriva-*
%{_iconsdir}/hicolor/*/apps/xterm-terminal.png
