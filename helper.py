from IPython import display
import matplotlib.pyplot as plt
import xlsxwriter


workbook = xlsxwriter.Workbook('data.xlsx')
worksheet1 = workbook.add_worksheet()
plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(0.1)

def graph(data):
    # data  = [[avg_time, score]]
    caption = 'TEST'
    worksheet1.set_column('A:C', 15)
    worksheet1.write('A1', caption)
    worksheet1.write('A3', 'Trials')
    worksheet1.write('B3', 'Average Time')
    worksheet1.write('C3', 'Score')
    worksheet1.add_table('A4:C154', {'data': data})
    workbook.close()
