const C = document.querySelector("canvas"),
    holst = C.getContext("2d"),
    holstWidth = C.width = innerWidth,
    holstHeight = C.height = innerHeight;

const letters = "A+Б0В-Г1Д=У2Ё3Е ЖЗ3 И4Й К5Л М6Р О8Н Р9С Ф21Ъ Т!У Ц?Ч Ш,ШЪ.Ы Ь:ЭЮ;Я",
    matrix = letters.split('');

let font = 11 ,
    col = holstWidth/font,
    arr=[];

for(let i =0;i<col;i++)
{
    arr[i] = 1;
}

function draw(){
    holst.fillStyle = "rgba(0,0,0,.07)";

    holst.fillRect(0,0,holstWidth,holstHeight);

    holst.fillStyle = "#0f0";

    holst.font = font + "px system-ui";

    for(let i = 0; i < arr.length; i++)
    {
        let txt = matrix[Math.floor(Math.random()*matrix.length)];

        holst.fillText(txt,i*font,arr[i]*font);

        if(arr[i]*font> holstHeight && Math.random()>0.975)
        {
            arr[i]=0;
        }

        arr[i]++;
    }


}
C.style.zIndex= -99
setInterval(draw,33)

