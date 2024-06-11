# pydistinstall - CLI utility

> List all execution stages

```python
py-distinstall --list-stages
```

> Unmount currently-mounted mount path

```python
sudo py-distinstall -m RELEASE -u [mount-point] {actions}
```

> Unmount the currently-mounted mount directory and begin the complete process (run every stage)

```python
sudo py-distinstall -m RELEASE -u [mount-point] start
```

> Unmount the currently-mounted mount directory and execute stages 1 to 10

```python
sudo py-distinstall -m RELEASE -u [mount-point] \
    --execute-stage 1 \    
    --execute-stage 2 \    
    --execute-stage 3 \   
    --execute-stage 4 \    
    --execute-stage 5 \    
    --execute-stage 6 \
    --execute-stage 7 \
    --execute-stage 8 \
    --execute-stage 9 \
    --execute-stage 10
```

> Execute Stage 1 : Check host system time zone

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 1
```

> Execute Stage 2 : Check host system Motherboard bootloader firmware (i.e. BIOS/UEFI)

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 2
```

> Execute Stage 3 : 

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 3
```

> Execute Stage 4 : Create and format disk filesystem table and partitions

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 4
```

> Execute Stage 5 : Mount partition scheme

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 5
```

> Execute Stage 6 : 

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 6
```

> Execute Stage 7 : Generate Chroot Filesystems Table (/etc/fstab)

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 7
```

> Execute Stage 8 : Chroot command execution

```python
sudo py-distinstall -m RELEASE --execute-stage 8
```

> Execute Stage 9 : Post-Installation

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 9
```

> Execute Stage 10 : Post-Installation Cleanup and Sanitization

```python
sudo py-distinstall -m RELEASE -u [mount-point] --execute-stage 10
```

