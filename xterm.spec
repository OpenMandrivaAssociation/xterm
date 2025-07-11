Summary:	The standard terminal emulator for the X Window System
Name:		xterm
Version:	401
Release:	1
License:	MIT
Group:		Terminals
Url:		https://invisible-island.net/xterm/
Source0:	https://invisible-mirror.net/archives/xterm/%{name}-%{version}.tgz
Source1:	%{name}.desktop
Source2:	failsafe.desktop
# from http://www.vim.org/scripts/script.php?script_id=1349, public domain
Source20:	colortest.pl
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	luit
Requires:	luit
BuildSystem:	autotools
BuildOption:	--disable-full-tgetent
BuildOption:	--enable-wide-chars
BuildOption:	--x-includes=%{_includedir}/freetype2
BuildOption:	--enable-luit
BuildOption:	--enable-256-color
BuildOption:	--with-app-defaults=%{_libdir}/X11/app-defaults
BuildOption:	--with-icon-theme=hicolor
BuildOption:	--with-icondir=%{_iconsdir}

%description
The XTerm program is the standard terminal emulator for the X Window System. It
provides DEC VT102/VT220 and Tektronix 4014 compatible terminals for programs
that can't use the window system directly. If the underlying operating system
supports terminal resizing capabilities (for example, the SIGWINCH signal in
systems derived from 4.3bsd), xterm will use the facilities to notify programs
running in the window whenever it is resized.

The xterm included in this package has support for 256 colors enabled.

%prep -a
cp %{SOURCE20} .

%install -a
# NOTE: encodingMode: locale means to follow the charset encoding of the
# locale. A quite complete unicode font is set as the default (instead of the
# very poor "fixed" one). a quick cat is used instead of patching the sources;
# it shoulmd be made the default imho
# locale: true means to use luit to convert locale encoding to unicode
# for display.
# luit support is needed for it to work -- pablo
cat << EOF >> %{buildroot}%{_libdir}/X11/app-defaults/XTerm

*.vt100.font: -misc-fixed-medium-r-normal--15-140-75-75-c-90-iso10646-1
*.vt100.encodingMode: locale
*.locale: true
*.PtyInitialErase: on
*.backarrowKeyIsErase: on
*.allowFontOps: false
*.allowTcapOps: false
*.disallowedWindowOps: 1,2,3,4,5,6,7,8,9,11,13,14,18,19,20,21,GetSelection,SetSelection,SetWinLines,SetXprop
EOF

# (tpg) install desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

# (tpg) use xterm as failsafe for xsession
mkdir -p %{buildroot}%{_datadir}/xsessions
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/xsessions/failsafe.desktop

for xpm in xterm{-color_32x32,-color_48x48,_32x32,_48x48}.xpm; do
    rm -f %{buildroot}%{_datadir}/pixmaps/$xpm
done

%files
%doc ctlseqs.txt colortest.pl
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/X11/app-defaults/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/xsessions/failsafe.desktop
%{_iconsdir}/hicolor/*/apps/*xterm*.*
%{_datadir}/pixmaps/*.xpm
