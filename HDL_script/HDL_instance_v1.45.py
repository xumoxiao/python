import sys 
import os 
import re

for arg in sys.argv:  
    print (arg) 
file_path = sys.argv[1]


#file_path = 'F:\\python_test\\test\\em_lib_tpm_template.vhd'
#file_path = 'F:\\python_test\\python\\HDL_script\\axi_10g_ethernet.vhd'
#file_path = 'C:\\Users\\FPGA\\Desktop\\0020_zynq_dma\\fw\\src\\axi_hp\\dma_axi_m_wr.vhd'
#file_path = 'C:\\Users\\FPGA\\Desktop\\0020_zynq_dma\\fw\\tb\\top_tc\\axi_s_hp_tc.v'

print(file_path)
#fp = open(file_path,'r',encoding = 'utf-8') 
fp = open(file_path,'r') 
file_name = os.path.basename(file_path)
print(file_name,'has opened')
print(file_name)
(shotname,extension) = os.path.splitext(file_name);
print(shotname)#shotname
file_line_list = fp.readlines() 

vlog_module_pattern = r'^\s*(?:\bmodule\b)\s*(\w+)(?:\s*[#()]*\s*)*'
vlog_port_pattern = r'^\s*(\binput|output|inout\b)\s*(?:wire|reg)*\s*(?:signed)*\s*(\[\S+\s*:\s*\S+\])*\s*(\w+)(?:\s*[,;]*\s*)'
vlog_param_pattern  = r'^\s*(?:\bparameter\b)\s*(\w+)\s*[=]\s*((\w+)(\'\w+)*)\s*[,]*\s*'


vhdl_module_pattern = r'^\s*(?:\bentity\b|\bENTITY\b)\s*(\w+)\s*(?:is|IS)\s*'
vhdl_start_pattern  = r'^\s*library|LIBRARY\s*\w+\s*[;]\s*'
vhdl_port_pattern   = r'^\s*(\w+)\s*(?:[:])\s*(in\b|IN\b|out\b|OUT\b|inout\b|inout\b)\s*(\w+)*\s*([(]\s*\S+\s*\-*\s*\w*\s*(?:downto|DOWNTO)\s*\S+\s*\-*\s*\w*\s*[)])*\s*[;]*\s*'
vhdl_param_pattern  = r'^\s*(\w+)\s*[:]\s*(\bpositive|integer|string|std_logic|std_logic_vector|boolean|POSITIVE|INTEGER|STRING|STD_LOGIC|STD_LOGIC_VECTOR|BOOLEAN\b)\s*([(]\s*\S+\s*\-*\s*\w*\s*(?:downto|DOWNTO)\s*\S+\s*\-*\s*\w*\s*[)])*\s*[:=]*\s*((\w+)*(["]\w+["])*)*\s*'
                        
vhdl_over_pattern   = r'^\s*END|end\s*\w+\s*[;]\s*'


# port attr = { dir , width , name , type }
# param attr = { name , type , width , value }
port_list = []
longest_len = 0
name_match = None
param_list = []
param_match = []

vlog_flag = False
vhdl_flag = False
vhdl_start_flag = False

print(param_list)
for file_line in file_line_list:

    # module name expression 
    if( name_match == None):
        name_match = re.match(vlog_module_pattern,file_line)
        if(name_match != None):
            print ('HDL is Verlog')
            module_name = name_match.group(1)
            vlog_flag = True
            continue
        name_match = re.match(vhdl_module_pattern, file_line)
        if (name_match != None):
            print('HDL is VHDL')
            module_name = name_match.group(1)
            vhdl_flag = True
            continue


    if( None != re.match(vhdl_start_pattern,file_line) and vhdl_start_flag == False):
        vhdl_start_flag = True
        print(vhdl_start_flag)
        print(file_line)
    #elif(vhdl_flag == True and vhdl_start_flag == True):
    #    print(file_line)
    if( None != re.match(vhdl_over_pattern,file_line) and vhdl_start_flag == True):
        vhdl_start_flag = False
        print('vhdl_over_flag')
        print(file_line)
    # port expression
    port_attr = []
    if( vlog_flag == True ):       
        line_match = re.match(vlog_port_pattern,file_line)
        if(line_match!=None):
            port_attr.append(line_match.group(1))
            port_attr.append(line_match.group(2))
            port_attr.append(line_match.group(3))
            port_attr.append('')
            port_list.append(port_attr)
            if(len(port_attr[2])>longest_len):
                longest_len = len(port_attr[2])
            #print(port_attr)

    elif ( vhdl_flag == True and vhdl_start_flag == True ):
        line_match = re.match(vhdl_port_pattern,file_line)
        if(line_match!=None):
            port_attr.append(line_match.group(2))
            port_attr.append(line_match.group(4))
            port_attr.append(line_match.group(1))
            port_attr.append(line_match.group(3))
            #print(line_match.group(3))
            port_list.append(port_attr)
            if(len(port_attr[2])>longest_len):
                    longest_len = len(port_attr[2])
    else:
        pass
   
    # param regular expression
    param_attr = []
    if( vlog_flag == True ):
        param_match = re.match(vlog_param_pattern,file_line)
        if( param_match != None ):
            param_attr.append(param_match.group(1))
            param_attr.append('')# verilog doesn't have type 
            param_attr.append('')# verilog doesn't have type width
            param_attr.append(param_match.group(2))
            param_list.append(param_attr)
            if(len(param_attr[0])>longest_len):
                longest_len = len(param_attr[0])
    elif ( vhdl_flag == True and vhdl_start_flag == True):
        param_match = re.match(vhdl_param_pattern,file_line)
        if( param_match != None ):
            param_attr.append(param_match.group(1))
            param_attr.append(param_match.group(2))# verilog doesn't have type 
            param_attr.append(param_match.group(3))# verilog doesn't have type width
            param_attr.append(param_match.group(4))
            param_list.append(param_attr)
            if(len(param_attr[0])>longest_len):
                longest_len = len(param_attr[0])
    else:
        pass


print(vhdl_start_flag)
print(len(port_list))
print(len(param_list))

if(vlog_flag == 0 and vhdl_flag == 0):
    print('Invalid File')
    input()

fp.close()
""" --------------------------------  Create file    ------------------------------- """


new_file_name = shotname+'.ins'
print(file_path)
print(os.path.split(file_path))
new_file_path = os.path.split(file_path)[0] + '\\'+new_file_name
print(new_file_path)
fp = open(new_file_path,'w')

#judge the name len
if(len(shotname)%2 == 0):
    pass
else:
    shotname = shotname + ' '

inst_name = 'Verlog inst '

""" --------------------------------  Verlog inst Start ------------------------------- """

fp.write('\n/*')
for x in range(96):
    fp.write('-')
fp.write('*/\n')
#second row
fp.write('/*')
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write(shotname)
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write('*/\n')

fp.write('/*')
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write(inst_name)
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write('*/\n')

#third row
fp.write('/*')
for x in range(96):
    fp.write('-')
fp.write('*/\n')


write_str = None
fp.write('\n/*\n')
fp.write(module_name)
fp.write('\n')
if(param_list!=[]):
    fp.write('#(\n')
    for i in range(len(param_list)):
        write_str = '\t.'+param_list[i][0]
        fp.write(write_str)
        for x in range( longest_len - len(param_list[i][0]) ):
            fp.write(' ')
        if(i == (len(param_list)-1)):
            write_str = '\t( '+param_list[i][0]+' )//'+param_list[i][3]+'\n'
        else:
            write_str = '\t( '+param_list[i][0]+' ),//'+param_list[i][3]+'\n'
        fp.write(write_str)
    fp.write(')\n')
if(port_list!=[]):
    fp.write(module_name)
    fp.write('_i\n(\n')
    for i in range(len(port_list)):
        if( port_list[i][1] == None ):
            port_list[i][1] = ''
        write_str = '\t.'+port_list[i][2]
        fp.write(write_str)
        for x in range( longest_len - len(port_list[i][2]) ):
            fp.write(' ')
        if( i == (len(port_list)-1) ):
            write_str = '\t( '+port_list[i][2]+' )//'+port_list[i][0]+' '+port_list[i][1]+'\n'
        else:
            write_str = '\t( '+port_list[i][2]+' ),//'+port_list[i][0]+' '+port_list[i][1]+'\n'
        fp.write(write_str)
fp.write(');\n*/')
print('verilog inst over')
""" --------------------------------  Verlog inst End  -------------------------------- """
#fp.close()
#input()

""" -----------------------  VHDL inst Start (No Component)  -------------------------- """
inst_name = 'VHDL Inst '
fp.write('\n')
for x in range(100):
    fp.write('-')
fp.write('\n--')
#second row
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write(shotname)
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write('--\n--')
#third row
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write(inst_name)
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write('--\n')

for x in range(100):
    fp.write('-')
fp.write('\n')

write_str = None
write_str = module_name+'_i :entity work.'+ module_name + '\n'
fp.write(write_str)
write_str = '--'+module_name+'_i : '+ module_name + '\n'
fp.write(write_str)
if( param_list != [] ):
    write_str = 'generic map(\n'
    fp.write(write_str)
    for i in range(len(param_list)):
        write_str = '\t'+param_list[i][0]
        fp.write(write_str)
        for x in range( longest_len - len(param_list[i][0]) ):
            fp.write(' ')
        if(i == (len(param_list)-1)):
            write_str = '\t=> '+param_list[i][0]+'--'+param_list[i][3]+'\n'
        else:
            write_str = '\t=> '+param_list[i][0]+',--'+param_list[i][3]+'\n'
        fp.write(write_str)
    fp.write(')\n')
if( port_list != [] ):
    fp.write('port map(\n')
    for i in range(len(port_list)):
        if( port_list[i][1] == None ):
            port_list[i][1] = ''
        write_str = '\t'+port_list[i][2]
        fp.write(write_str)
        for x in range( longest_len - len(port_list[i][2]) ):
            fp.write(' ')
        if( i == (len(port_list)-1) ):
            write_str = '\t=> '+port_list[i][2]+'--'+port_list[i][0]+' '+port_list[i][1]+'\n'
        else:
            write_str = '\t=> '+port_list[i][2]+',--'+port_list[i][0]+' '+port_list[i][1]+'\n'
        fp.write(write_str)
fp.write(');\n')
""" -----------------------  VHDL inst End   (No Component)  -------------------------- """
#fp.close()
#input()
""" ---------------------------  VHDL Component Start  -------------------------------- """
inst_name = 'VHDL Component'


fp.write('\n')
for x in range(100):
    fp.write('-')
fp.write('\n--')
#second row
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write(shotname)
for x in range(48-int(len(shotname)/2)):
    fp.write(' ')
fp.write('--\n--')
#third row
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write(inst_name)
for x in range(48-int(len(inst_name)/2)):
    fp.write(' ')
fp.write('--\n')

for x in range(100):
    fp.write('-')
fp.write('\n')

if(vlog_flag == True):
    fp.write('\n')
    fp.write(' ----------------- Verlog Component has error --------------------')
    fp.write('\n\n')

write_str = None
write_str = 'component '+ module_name + '\n'
fp.write(write_str)
if( param_list != [] ):
    write_str = 'generic (\n'
    fp.write(write_str)
    for i in range(len(param_list)):
        write_str = '\t'+param_list[i][0]
        fp.write(write_str)
        if(param_list[i][2] == None):
            param_list[i][2] = ''
        for x in range( longest_len - len(param_list[i][0]) ):
            fp.write(' ')
        if(i == (len(param_list)-1)):
            write_str = '\t: '+param_list[i][1]+param_list[i][2]+' := '+param_list[i][3]+'\n'
        else:
            write_str = '\t: '+param_list[i][1]+param_list[i][2]+' := '+param_list[i][3]+';\n'
        fp.write(write_str)
    fp.write(');\n')

if( port_list != [] ):
    fp.write('port (\n')
    # port attr = { dir , width , name , type }
    for i in range(len(port_list)):
        #dir
        if( port_list[i][0] == None ):
            port_list[i][0] = ''
        elif(port_list[i][0] == 'input'):
            port_list[i][0] = 'in '
        elif(port_list[i][0] == 'output'):
            port_list[i][0] = 'out'

        #width
        if( port_list[i][1] == None ):
            port_list[i][1] = ''

        #name
        if( port_list[i][2] == None ):
            port_list[i][2] = ''

        #type
        if( port_list[i][3] == None or port_list[i][3] == '' ):
            if( port_list[i][1] == '' ):
                port_list[i][3] = 'std_logic'
            elif( port_list[i][1] != '' ):
                port_list[i][3] = 'std_logic_vector'

        write_str = '\t'+port_list[i][2]
        fp.write(write_str)
        for x in range( longest_len - len(port_list[i][2]) ):
            fp.write(' ')
        if( i == (len(port_list)-1) ):
            write_str = '\t: '+port_list[i][0]+' '+port_list[i][3]+port_list[i][1]+'\n'
        else:
            write_str = '\t: '+port_list[i][0]+' '+port_list[i][3]+port_list[i][1]+';\n'
        fp.write(write_str)
fp.write(');\n')
fp.write('end component;')
""" ---------------------------   VHDL Component End   -------------------------------- """
fp.close()

#input()

