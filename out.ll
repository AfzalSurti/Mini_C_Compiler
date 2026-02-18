; --- MiniC LLVM IR ---
declare i32 @printf(i8*,...)
@.fmt = private unnamed_addr constant [4 x i8] c"%d\0A\00"

define i32 @main(){
entry:
%1=add i32 5,6
  %a=alloca i32
store i32 %1, i32* %a
%2=load i32,i32*%a
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.fmt, i32 0, i32 0), i32 %2)
  ret i32 0
}