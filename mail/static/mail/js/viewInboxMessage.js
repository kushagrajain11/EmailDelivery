var y = (function()
{
	var items, to, subject, body, from, dateTime, reply, forward, del, download, image, imageAnchor, currentDate;

	function getRequestURL(messageID){
		return ('/mail/getMessage/' + messageID);
	}

	function getReplyURL(senderID){
		return ('/mail/' + senderID + '/reply');
	}

	function getForwardURL(messageID){
		return ('/mail/' + messageID + '/forward');
	}

	function sendRequest(messageID, date){
		$.ajax({
			url : getRequestURL(messageID),
			type : 'GET',
			success : function(data){ reOrganize(data, date); },
			error: function(error){ console.log(error); }
		});
	}

	function reOrganize(data, date){
		var space = ':&nbsp&nbsp&nbsp&nbsp ';

		to.innerHTML = (space + data.response.recipients);
		from.innerHTML = (space + data.response.from);
		dateTime.innerHTML = ':&nbsp&nbsp&nbsp' + date;
		subject.innerHTML = (space + data.response.subject);
		body.innerHTML = data.response.body;

		reply.setAttribute('href', getReplyURL(data.response.senderID));
		forward.setAttribute('href', getForwardURL(data.response.messageID));

		if(data.response.url.length == 0){
			imageAnchor.style.display = 'none';
			imageAnchor.setAttribute('href', '#');
			download.style.display = 'none';
			image.setAttribute('src', '');
		}

		else{
			imageAnchor.style.display = 'block';
			imageAnchor.setAttribute('href', data.response.url);
			download.style.display = 'inline';
			image.setAttribute('src', data.response.url);
			download.setAttribute('address', data.response.path);
		}
	}

	function createImage(){
		var container = document.getElementById('mainContainer');
		var string = "Download&nbsp <i class='fa fa-download' aria-hidden='true'></i>";

		image = document.createElement('img');
		imageAnchor = document.createElement('a');
		imageAnchor.setAttribute('href', '#');
		imageAnchor.setAttribute('id', 'anchor');
		imageAnchor.setAttribute('target', '_blank');
		imageAnchor.appendChild(image);
		imageAnchor.style.display = 'none';

		download = document.createElement('a');
		download.setAttribute('href', '#');
		download.setAttribute('id', 'download');
		download.innerHTML = string;
		download.style.display = 'none';
		download.addEventListener('click', x.sendRequest);

		container.insertBefore(imageAnchor, reply);
		container.insertBefore(download, reply);
	}


	function init(obj){
		var x = document.querySelectorAll('#mainContainer > div > p');
		items = document.querySelectorAll('#' + obj.list + ' > li > a');
		body = document.querySelectorAll('#mainContainer > div');

		body 		= body	[body.length - 1];
		to 			= x[0];
		from 		= x[1];
		dateTime 	= x[2];
		subject 	= x[3];
		reply 		= document.getElementById(obj.reply);
		forward 	= document.getElementById(obj.forward);
		del 		= document.getElementById(obj.del);
		download 	= document.getElementById(obj.download);
		image 		= document.querySelector('#' + obj.anchor + ' > img');
		imageAnchor = document.getElementById(obj.anchor);

		if(!image)
			createImage();

		for(var i = 0; i < items.length; i++)
			items[i].addEventListener('click', sendRequest.bind(this, items[i].getAttribute('messageID'), items[i].innerText));
	}

	return {
		init : init,
	};
})();