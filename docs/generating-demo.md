# Documentations - Generating demo animations

## Demo Properties/Specifications
- Fonts
    - Font Family: JetBrainsMono (Nerd Font Patched)
        + Full Theme: "JetBrainsMono Nerd Font Mono,JetBrainsMono NFM,JetBrainsMono NFM ExtraBold"

- asciinema-agg
    + Theme: monokai

## Methods and Tools
- Using 'asciinema' and 'asciinema-agg' separately
    - Use 'asciinema' to record the terminal screen into a recording file
        ```bash
        sudo asciinema -c "py-distinstall -m RELEASE start" output.cast
        ```
    - Use 'asciinema-agg' to convert the terminal screen recording into animation gif
        ```bash
        agg --theme monokai --font-family "JetBrainsMono Nerd Font Mono,JetBrainsMono NFM,JetBrainsMono NFM ExtraBold" output.cast output.gif
        ```

- Using 'asciinema-util'
    - Explanation
        + asciinema-util, found in the repository [Thanatisia/py-utilities](https://github.com/Thanatisia/py-utilities), is my asciinema + asciinema-apg wrapper that aims to fuse both CLI utilities together
        - Parameters and Arguments
            - record
                + `--output-terminal-rec-filename output.cast` : Specify the terminal screen recording output filename
                + `--asciinema-opts "--overwrite"` : Passthrough the '--overwrite' flag into asciinema to overwrite the existing file
                + `-c [command]` : Execute the specified command
            - convert : Convert the terminal screen recording file into a demo animation gif file
                + `--theme monokai` : using a monokai-themed background 
                + `--input-terminal-rec-filename output.cast` : Specify the target terminal screen recording file you want to use to convert into the animation gif 
                + `--output-animation-filename output.gif` : Specify the animation gif output filename 
                + `--asciinema-agg-opts "--font-family JetBrainsMono Nerd Font Mono,JetBrainsMono NFM,JetBrainsMono NFM ExtraBold"` : : Passthrough the '--font-family' arguments into asciinema-agg using 'JetBrainsMono' (Nerd Fonts Patched) as the font family
    - Execute and passthrough the command into the utility and conver the terminal recording into the demo gif
        ```bash
        sudo asciinema-util \
            record --output-terminal-rec-filename output.cast --asciinema-opts "--overwrite" -c "py-distinstall -m RELEASE start" \
            convert --theme monokai --input-terminal-rec-filename output.cast --output-animation-filename output.gif --asciinema-agg-opts "--font-family JetBrainsMono Nerd Font Mono,JetBrainsMono NFM,JetBrainsMono NFM ExtraBold"
        ```

