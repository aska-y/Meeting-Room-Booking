import json
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import DeleteView

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import *
from .forms import *

#ホーム
class HomeView(ListView):
    model = Room
    template_name = 'core/home.html'

#会議室個別ページ
class RoomView(DetailView, FormMixin):
    model = Room
    template_name = 'core/room.html'
    form_class = BookingForm
    
    def get_context_data(self, **kwargs):
        # オブジェクト情報をcontextに入れる
        context = super().get_context_data(**kwargs)
        room_list = Room.objects.all()
        context.update({'room_list': room_list})

        #その部屋の予約情報querysetを取得し、eventsという名称でjsonにしてcontextに入れる
        room_pk = self.kwargs.get('pk')
        booking_qs = Booking.objects.filter(room_id=room_pk)
        events = []
        for booking in booking_qs:
            event = {
                'id': booking.id,
                'title': booking.title,
                'start': booking.start_time.isoformat(timespec = 'seconds'),
                'end': booking.end_time.isoformat(timespec = 'seconds'),
                'backgroundColor': '#98c1d9',
                'borderColor': '#6190ab',
            }
            events.append(event)
            context.update({'events': json.dumps(events)})
        
        return context

    #予約フォーム
    def post(self, *args, **kwargs):
        form = BookingForm(self.request.POST)
        if form.is_valid:
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    #予約ボタン押下後は元のページに戻る
    def get_success_url(self):
        room_pk = self.kwargs.get('pk')
        return reverse_lazy('room', args=(room_pk, ))


#予約の削除
def delete_event(request, event_id):
    if request.method == 'POST': # または DELETE メソッド
        # event = get_object_or_404(Booking, id = event_id)
        # event.delete()
        # return JsonResponse({'status': 'success'})
    # return JsonResponse({'status': 'error'}, status=400)
        try:
            event = Booking.objects.get(id = event_id)
            event.delete()
            return JsonResponse({'status': 'success', 'message': 'イベントを削除しました'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'イベントが見つかりません'}, status = 404)


# class EventDeleteView(DeleteView):
#     model = Room
#     template_name = 'core/room.html'
#     success_url = reverse_lazy('room', args=(room_pk, ))

#     def delete_event(request, event_id):
#         room_pk = self.kwargs.get('pk')
#         return super().delete(request, *args, **kwargs)
